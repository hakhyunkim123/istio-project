from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('front/createTodo/',views.create_todo, name='createTodo'),
    path('front/deleteTodo/', views.done_todo, name='deleteTodo'),
    path('proj/<int:project_id>/', views.goto_proj, name = 'gotoProj'),
    path('front/', views.front, name = 'front'),

    path('login/', views.login, name = 'login'),

# ============================================================================================================================ #
    path('addproj/', views.add_project, name = 'addProject'),
    path('invite/<int:project_id>', views.invite, name = 'invite'),
# ============================================================================================================================ #

    path('notice_list/<int:project_id>/', views.notice_list, name = 'notice_list'),
    path('notice/post/<int:notice_id>/<int:project_id>', views.notice_detail, name = 'notice_detail'),
    path('notice/edit/<int:notice_id>/<int:project_id>', views.notice_edit, name = 'notice_edit'),
    path('notice/delete/<int:notice_id>/<int:project_id>', views.notice_delete, name = 'notice_delete'),
    path('notice/new/<int:project_id>/', views.notice_new, name = 'notice_new'),
    path('chat/', views.goto_chat, name='gotoChat'),
]
