from django.db import models
from django.contrib.auth.models import User

# Group Model
class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Membership Model to represent user-group relationships
class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='members', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"


class Chat(models.Model):
    group = models.ForeignKey(Group, related_name='chats', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}: {self.content[:30]}'
    
    class Meta:
        ordering = ['timestamp']






from django.utils.timezone import now

class Message(models.Model):
    content = models.TextField()
    # timestamp = models.DateTimeField( auto_now_add=True)
    sender = models.CharField(max_length=100)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="messages")



# Chat Model for storing individual and group messages
# class Chat(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     group = models.ForeignKey(Group, related_name='chats', null=True, blank=True, on_delete=models.CASCADE)
#     recipient = models.ForeignKey(User, related_name='private_chats', null=True, blank=True, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         if self.group:
#             return f"Group message from {self.sender.username} in {self.group.name}"
#         return f"Private message from {self.sender.username} to {self.recipient.username}"

#     class Meta:
#         ordering = ['created_at']
