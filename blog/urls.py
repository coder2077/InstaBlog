from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    HomePageView, 
    CreatePostView, 
    UpdatePostView, 
    DeletePostView, 
    PostDetailsView, 
)


urlpatterns = [
    path('posts/<int:pk>/', PostDetailsView.as_view(), name='post_details'), 
    path('posts/<int:pk>/delete/', DeletePostView.as_view(), name='delete_post'), 
    path('posts/<int:pk>/edit/', UpdatePostView.as_view(), name='edit_post'), 
    path('new/', CreatePostView.as_view(), name='new_post'), 
    path('', HomePageView.as_view(), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

