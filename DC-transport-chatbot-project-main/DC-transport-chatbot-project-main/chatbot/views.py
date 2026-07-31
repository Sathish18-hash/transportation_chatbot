from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

import markdown

from .models import Chat, Message
from .gemini import ask_gemini


def home(request):

    chats = Chat.objects.order_by(
        "-created_at"
    )

    if chats.exists():

        return redirect(
            "chat",
            chat_id=chats.first().id,
        )

    return redirect(
        "new_chat"
    )


def new_chat(request):

    chat = Chat.objects.create(
        title="New Chat"
    )

    return redirect(
        "chat",
        chat_id=chat.id,
    )


def chat_page(request, chat_id):

    chat = get_object_or_404(
        Chat,
        id=chat_id,
    )

    chats = Chat.objects.order_by(
        "-created_at"
    )

    messages = chat.messages.order_by(
        "created_at"
    )

    if request.method == "POST":

        user_message = (
            request.POST
            .get("message", "")
            .strip()
        )

        if user_message:

            Message.objects.create(
                chat=chat,
                sender="user",
                message=user_message,
            )

            try:

                bot_response = ask_gemini(
                    user_message
                )

            except Exception as error:

                print(
                    "Gemini Error:",
                    error,
                )

                bot_response = (
                    "Sorry, the chatbot is "
                    "temporarily unavailable. "
                    "Please try again."
                )

            bot_response_html = (
                markdown.markdown(
                    bot_response,
                    extensions=[
                        "tables",
                    ],
                )
            )

            Message.objects.create(
                chat=chat,
                sender="bot",
                message=bot_response_html,
            )

            if chat.title == "New Chat":

                chat.title = (
                    user_message[:35]
                )

                chat.save()

        return redirect(
            "chat",
            chat_id=chat.id,
        )

    return render(
        request,
        "chatbot/chat.html",
        {
            "chat": chat,
            "chats": chats,
            "messages": messages,
        },
    )


def delete_chat(request, chat_id):

    chat = get_object_or_404(
        Chat,
        id=chat_id,
    )

    if request.method == "POST":

        chat.delete()

    return redirect(
        "home"
    )