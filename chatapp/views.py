from django.shortcuts import render, HttpResponse

# from chatapplication.chatapp.models import Group


from .models import Group,Message



# Create your views here.
def home(request):
    groups = Group.objects.all()  # Fetch all groups
    group_id = request.GET.get('group', None)  # Get the group ID from the query params

    if group_id:
        group = Group.objects.get(id=group_id)
        messages = Message.objects.filter(group=group)
    else:
        group = None
        messages = []
    return render(request, 'home.html',{'groups':groups,group:group,'messages':messages})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Group, Chat
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.timezone import now


from django.shortcuts import render, redirect
from .models import Group, Message
from django.contrib.auth.models import User

def send_message(request):
    if request.method == "POST":
        message_text = request.POST['message']
        group_id = request.GET.get('group')
        group = Group.objects.get(id=group_id)
        sender = request.user  # Assuming the user is logged in
        
        Message.objects.create(sender=sender, group=group, text=message_text)
        
        return redirect(f'/?group={group_id}')


from django.http import JsonResponse
from .models import Group, Message

def group_messages(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        # Correcting the query to use the correct join for 'sender' field
        messages = Message.objects.filter(group=group).select_related('sender').values('content','sender')

        message_data = list(messages)  # Convert queryset to list for JSON serialization
        return JsonResponse({'messages': message_data})

    except Group.DoesNotExist:
        return JsonResponse({'error': 'Group not found'}, status=404)
    
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_id = data.get('group_id')
        content = data.get('content')

        try:
            group = Group.objects.get(id=group_id)
            user = request.user  # Assuming the user is logged in

            # Create a new message
            message = Message.objects.create(
                group=group,
                sender=user,
                content=content,
            )

            return JsonResponse({'success': True})
        except Group.DoesNotExist:
            return JsonResponse({'error': 'Group not found'}, status=404)