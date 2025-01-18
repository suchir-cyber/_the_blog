from django.urls import path
from .views import PostListView, PostDetailView , PostCreateView , PostUpdateView , PostDeleteView , UserPostListView ,SearchView
from . import views


urlpatterns = [
    path('', PostListView.as_view(),name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_id>/vote/<str:vote_type>/', views.toggle_vote, name='toggle_vote'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/',views.about,name='blog-about'),
    path('help/',views.contact,name='blog-contact'),
    path('searchbar/',SearchView.as_view(),name='searchbar')
]
