from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home",
    ),

    path(
        "new-chat/",
        views.new_chat,
        name="new_chat",
    ),

    path(
        "chat/<int:chat_id>/",
        views.chat_page,
        name="chat",
    ),

    path(
        "delete-chat/<int:chat_id>/",
        views.delete_chat,
        name="delete_chat",
    ),

]