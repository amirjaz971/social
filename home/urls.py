from django.urls import path
from . import views

app_name='home'
urlpatterns = [
    path('',views.Home.as_view(),name='home'),
    path('post/<int:post_id>/<slug:post_slug>/',views.Post_detail.as_view(),name='post_detail'),
    path('post/delete/<int:post_id>/',views.Delete.as_view(),name='delete'),
    path('post/update/<int:post_id>/',views.Update.as_view(),name='update'),
    path('post/create/',views.Create.as_view(),name='create'),
    
]
