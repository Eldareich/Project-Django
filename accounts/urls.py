from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('reset_password_validate/<uidb64>/<token>/',
         views.reset_password_validate, name='reset_password_validate'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),

    path('profile/', views.profile_view, name='profile'),
    path('<username>/', views.profile_view, name='userprofile'),
    path('profile/edit', views.profile_edit_view, name='profile-edit'),
    path('profile/delete', views.profile_delete_view, name='profile-delete'),
    path('profile/registercreate/', views.profile_edit_view,
         name='profile-registercreate'),
]
