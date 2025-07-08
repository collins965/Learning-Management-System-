from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST

from .models import ChatGroup, ChatMessage
from core.models import Lesson, Quiz


# -------------------------------
# Inbox View (Updated)
# -------------------------------
@login_required
def inbox(request):
    query = request.GET.get('q', '')
    groups = ChatGroup.objects.filter(members=request.user)

    if query:
        groups = groups.filter(name__icontains=query)

    group_unread_counts = {
        group.id: group.messages.filter(is_read=False).exclude(sender=request.user).count()
        for group in groups
    }

    direct_messages = []
    group_chats = []

    for group in groups:
        group._current_user_id = request.user.id  # For __str__ or template display logic
        if group.is_private:
            group.other_user = group.get_other_member(request.user)
            direct_messages.append(group)
        else:
            group_chats.append(group)

    lessons = Lesson.objects.all()
    quizzes = Quiz.objects.all()

    return render(request, 'chat/inbox.html', {
        'direct_messages': direct_messages,
        'group_chats': group_chats,
        'group_unread_counts': group_unread_counts,
        'lesson_list': lessons,
        'quiz_list': quizzes,
    })


# -------------------------------
# Group Chat View
# -------------------------------
@login_required
def group_chat(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)

    # Mark unread messages as read
    ChatMessage.objects.filter(group=group, is_read=False).exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            ChatMessage.objects.create(group=group, sender=request.user, content=content)
            return redirect('chat:group_chat', group_id=group.id)

    messages = ChatMessage.objects.filter(group=group).order_by('timestamp')
    is_group_admin = group.is_admin(request.user)

    return render(request, 'chat/group_chat.html', {
        'group': group,
        'messages': messages,
        'is_group_admin': is_group_admin,
    })


# -------------------------------
# Create Group (with Admin)
# -------------------------------
@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            group = ChatGroup.objects.create(
                name=name,
                created_by=request.user,
                is_private=False
            )
            group.members.add(request.user)
            group.admins.add(request.user)
            return redirect('chat:group_chat', group_id=group.id)
    return render(request, 'chat/create_group.html')


# -------------------------------
# Manage Group (Admin Only)
# -------------------------------
@login_required
def manage_group(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)

    if not group.is_admin(request.user):
        return redirect('chat:group_chat', group_id=group.id)

    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)

        if action == "add_member":
            group.members.add(user)
        elif action == "make_admin":
            group.admins.add(user)

    non_members = User.objects.exclude(id__in=group.members.all())

    return render(request, "chat/manage_group.html", {
        "group": group,
        "members": group.members.all(),
        "admins": group.admins.all(),
        "non_members": non_members,
    })


# -------------------------------
# Join Public Group
# -------------------------------
@login_required
def join_group(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)
    group.members.add(request.user)
    return redirect('chat:group_chat', group_id=group.id)


# -------------------------------
# Browse Public Groups
# -------------------------------
@login_required
def browse_groups(request):
    groups = ChatGroup.objects.exclude(members=request.user)
    return render(request, 'chat/browse_groups.html', {'groups': groups})


# -------------------------------
# User Search (For DMs)
# -------------------------------
@login_required
def user_search(request):
    query = request.GET.get("q", "")
    users = User.objects.filter(Q(username__icontains=query)).exclude(id=request.user.id) if query else User.objects.none()
    return render(request, "chat/user_search.html", {"users": users, "query": query})


# -------------------------------
# Start or Continue Private Chat
# -------------------------------
@login_required
def start_chat_with_user(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if request.user == other_user:
        return redirect('chat:inbox')

    group_name = f"chat-{min(request.user.id, other_user.id)}-{max(request.user.id, other_user.id)}"

    group, created = ChatGroup.objects.get_or_create(
        name=group_name,
        defaults={'is_private': True, 'created_by': request.user}
    )

    group.members.add(request.user, other_user)
    return redirect('chat:group_chat', group_id=group.id)


# -------------------------------
# Delete Message (AJAX)
# -------------------------------
@login_required
@require_POST
def delete_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id, sender=request.user)
    message.delete()
    return JsonResponse({'success': True})


# -------------------------------
# Edit Message (AJAX)
# -------------------------------
@login_required
@require_POST
def edit_message(request, message_id):
    message = get_object_or_404(ChatMessage, id=message_id, sender=request.user)
    new_content = request.POST.get('content')
    if new_content:
        message.content = new_content
        message.save()
        return JsonResponse({'success': True, 'new_content': new_content})
    return JsonResponse({'success': False}, status=400)
