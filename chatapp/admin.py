from django.contrib import admin
from .models import Group, Membership, Chat,Message

# Models here
admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(Chat)
admin.site.register(Message)
