from django.db import models
from django.contrib.auth.models import User

class ChatGroup(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name='chat_groups')
    admins = models.ManyToManyField(User, related_name='admin_groups', blank=True)
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.is_private and self.members.count() == 2 and hasattr(self, '_current_user_id'):
            other = self.members.exclude(id=self._current_user_id).first()
            return f"DM with {other.username}" if other else "Private Chat"
        return self.name

    def get_other_member(self, user):
        """For private chats: returns the other user."""
        return self.members.exclude(id=user.id).first()

    def is_admin(self, user):
        """Check if a user is an admin of the group."""
        return self.admins.filter(id=user.id).exists()

    def get_last_message(self):
        """Returns the latest message sent in the group."""
        return self.messages.last()


class ChatMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # ✅ Track read status

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"

    class Meta:
        ordering = ['timestamp']  # ✅ Order messages by oldest first
