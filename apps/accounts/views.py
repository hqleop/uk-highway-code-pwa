from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.rules.models import Rule

from .forms import ProfileForm, RegisterForm
from .models import UserNote, UserProgress


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome. Your progress and notes are now saved.")
            return redirect("accounts:profile")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("core:home")


@login_required
def profile(request):
    profile_obj = request.user.userprofile
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=profile_obj)

    progress = UserProgress.objects.filter(user=request.user).select_related("section")
    notes = UserNote.objects.filter(user=request.user).select_related("rule", "rule__section")[:8]
    return render(
        request,
        "accounts/profile.html",
        {"form": form, "profile": profile_obj, "progress": progress, "notes": notes},
    )


@login_required
@require_POST
def add_note(request):
    rule = get_object_or_404(Rule, pk=request.POST.get("rule_id"))
    content = request.POST.get("content", "").strip()
    if not content:
        return JsonResponse({"ok": False, "error": "Note content is required."}, status=400)
    note = UserNote.objects.create(user=request.user, rule=rule, content=content)
    return JsonResponse({"ok": True, "note": note.content, "updated_at": note.updated_at.isoformat()})


@login_required
@require_POST
def toggle_notifications(request):
    profile_obj = request.user.userprofile
    profile_obj.push_notifications_enabled = not profile_obj.push_notifications_enabled
    profile_obj.save(update_fields=["push_notifications_enabled"])
    return JsonResponse({"ok": True, "enabled": profile_obj.push_notifications_enabled})
