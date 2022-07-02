from django.urls import path
from .views import SignUpView, userProfileView, userProfileEditView, userPostsListView, userSavedPostsListView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='signup'), 
    path('login/', LoginView.as_view(), name='login'), 
    path('profile/<str:username>/', userProfileView, name='profile'), 
    path('edit-profile/', userProfileEditView, name='edit_profile'), 
    path('profile/<str:username>/posts/', userPostsListView, name='user_posts'), 
    path('saved-posts/', userSavedPostsListView, name='saved_posts'),
]
