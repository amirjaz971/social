from django.urls import path
from . import views

app_name='account'
urlpatterns = [
    path('register/',views.Register.as_view(),name='register'),
    path('login/',views.User_login.as_view(),name='login'),
    path('logout/',views.User_logout.as_view(),name='logout'),
    path('profile/<int:user_id>/',views.User_profile.as_view(),name='profile'),
    path('follow/<int:user_id>/',views.Follow.as_view(),name='follow'),
    path('unfollow/<int:user_id>/',views.Unfollow.as_view(),name='unfollow'),
]