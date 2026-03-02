from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message

# Create your views here.

User = get_user_model()

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id) #grabs everyone except the person logged in
    return render(request, "user_list.html", {"users": users})

# @login_required
# def chat_page(request, user_id):
#     other_user = User.objects.get(id=user_id)

#     messages = Message.objects.filter(
#         sender__in=[request.user, other_user], #Find messages where the sender is either me or my friend.
#         receiver__in=[request.user, other_user] #ensures we aren't pulling in messages sent to other people.
#     ).order_by("timestamp")

#     return render(request, "chat.html", {
#         "other_user": other_user,
#         "messages": messages
#     })

# @login_required
# def chat_page(request, user_id):
#     other_user = User.objects.get(id=user_id)

#     # if request.method == "POST":
#     #     content = request.POST.get("message")

#     #     if content:  # prevent empty messages
#     #         Message.objects.create(
#     #             sender=request.user,
#     #             receiver=other_user,
#     #             content=content
#     #         )

#     messages = Message.objects.filter(
#         sender__in=[request.user, other_user],
#         receiver__in=[request.user, other_user]
#     ).order_by("timestamp")

#     return render(request, "chat.html", {
#         "other_user": other_user,
#         "messages": messages
#     })

@login_required
def chat_page(request, user_id):
    other_user = User.objects.get(id=user_id)

    # Mark unread messages as read
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("timestamp")

    return render(request, "chat.html", {
        "other_user": other_user,
        "messages": messages
    })