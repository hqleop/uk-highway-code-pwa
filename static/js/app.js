function csrfToken(form) {
  const input = form.querySelector("[name=csrfmiddlewaretoken]");
  return input ? input.value : "";
}

function iconize() {
  document.querySelectorAll("[data-icon]").forEach(el => {
    if (el.querySelector("svg")) return;
    const icon = document.createElement("i");
    icon.setAttribute("data-lucide", el.dataset.icon);
    el.prepend(icon);
  });
  if (window.lucide) window.lucide.createIcons();
}

function bindQuizStart() {
  const form = document.querySelector("[data-quiz-start]");
  if (!form) return;
  form.addEventListener("submit", async event => {
    event.preventDefault();
    const status = form.querySelector("[data-form-status]");
    status.textContent = "Starting...";
    const response = await fetch("/quiz/start/", {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken(form) },
      body: new FormData(form)
    });
    const data = await response.json();
    if (data.ok) {
      window.location.href = data.redirect_url;
    } else {
      status.textContent = data.error || "Could not start quiz.";
    }
  });
}

function renderQuestion(card, question) {
  card.querySelector("[data-question-text]").textContent = question.text;
  card.querySelector("[data-question-id]").value = question.id;
  const answers = card.querySelector("[data-answers]");
  answers.innerHTML = "";
  question.answers.forEach(answer => {
    const label = document.createElement("label");
    label.className = "answer-option";
    label.innerHTML = `<input type="radio" name="answer_id" value="${answer.id}" required><span></span>`;
    label.querySelector("span").textContent = answer.text;
    answers.appendChild(label);
  });
}

function bindAnswerForms() {
  document.querySelectorAll("[data-answer-form]").forEach(form => {
    form.addEventListener("submit", async event => {
      event.preventDefault();
      const feedback = document.querySelector("[data-feedback]");
      const response = await fetch("/quiz/answer/", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken(form) },
        body: new FormData(form)
      });
      const data = await response.json();
      feedback.hidden = false;
      feedback.className = `feedback ${data.is_correct ? "success" : "danger"}`;
      feedback.textContent = data.is_correct ? "Correct. " : `Not quite. Correct answer: ${data.correct_answer}. `;
      feedback.textContent += data.explanation || "";
      setTimeout(() => {
        if (data.completed) {
          window.location.href = data.results_url;
        } else if (data.next_question) {
          renderQuestion(document.querySelector("[data-quiz-session]"), data.next_question);
          feedback.hidden = true;
          form.reset();
        }
      }, 1300);
    });
  });
}

function bindDaily() {
  const form = document.querySelector("[data-daily-form]");
  if (!form) return;
  form.addEventListener("submit", async event => {
    event.preventDefault();
    const feedback = document.querySelector("[data-feedback]");
    const response = await fetch("/daily/answer/", {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken(form) },
      body: new FormData(form)
    });
    const data = await response.json();
    feedback.hidden = false;
    feedback.className = `feedback ${data.is_correct ? "success" : "danger"}`;
    feedback.textContent = data.ok
      ? `${data.is_correct ? "Correct." : `Not quite. Correct answer: ${data.correct_answer}.`} ${data.explanation || ""}`
      : data.error || "Could not save the answer.";
    form.querySelectorAll("input, button").forEach(el => (el.disabled = true));
  });
}

function bindNotes() {
  const form = document.querySelector("[data-note-form]");
  if (!form) return;
  form.addEventListener("submit", async event => {
    event.preventDefault();
    const response = await fetch("/accounts/notes/add/", {
      method: "POST",
      headers: { "X-CSRFToken": csrfToken(form) },
      body: new FormData(form)
    });
    const data = await response.json();
    if (!data.ok) return;
    const note = document.createElement("p");
    note.textContent = data.note;
    document.querySelector("[data-note-list]").prepend(note);
    form.reset();
  });
}

function urlBase64ToUint8Array(base64String) {
  const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, "+").replace(/_/g, "/");
  const rawData = window.atob(base64);
  return Uint8Array.from([...rawData].map(char => char.charCodeAt(0)));
}

function bindPush() {
  const button = document.querySelector("[data-enable-push]");
  if (!button) return;
  button.addEventListener("click", async () => {
    if (!window.HIGHWAY_CODE.vapidPublicKey || !("serviceWorker" in navigator) || !("PushManager" in window)) {
      button.textContent = "Push is not configured";
      return;
    }
    const registration = await navigator.serviceWorker.ready;
    const subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(window.HIGHWAY_CODE.vapidPublicKey)
    });
    await fetch("/notifications/subscribe/", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value },
      body: JSON.stringify(subscription)
    });
    button.textContent = "Push enabled";
  });
}

document.addEventListener("DOMContentLoaded", () => {
  iconize();
  bindQuizStart();
  bindAnswerForms();
  bindDaily();
  bindNotes();
  bindPush();
});
