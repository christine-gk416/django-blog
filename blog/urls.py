from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import profile

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('profile/', profile, name='users-profile'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
    path('dislike/<slug:slug>/', views.PostDisike.as_view(), name='post_dislike'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
