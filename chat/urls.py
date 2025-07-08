from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('group/<int:group_id>/', views.group_chat, name='group_chat'),
    path('create/', views.create_group, name='create_group'),
    path('join/<int:group_id>/', views.join_group, name='join_group'),
    path('browse/', views.browse_groups, name='browse_groups'),
    path('search-users/', views.user_search, name='user_search'),
    path('start-chat/<int:user_id>/', views.start_chat_with_user, name='start_chat_with_user'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('group/<int:group_id>/manage/', views.manage_group, name='manage_group'),
]
