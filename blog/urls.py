from django.urls import path
from django.conf import settings


from . import views
from .views import profile, ChangePasswordView, PostList

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('post-form/', views.PostCreateView.as_view(), name='create_post'),
    path('profile/', profile, name='users-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
    path('dislike/<slug:slug>/', views.PostDisike.as_view(), name='post_dislike'),
] 
