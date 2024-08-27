from django.urls import path
from blogs import views

urlpatterns = [
    # Endpoint for listing all blogs
    path('', views.BlogListAPIView.as_view(), name='blog_list'),
    # Endpoint for creating a blog
    path('create/', views.BlogCreateView.as_view(), name='blog-create'),
    # Endpoint for retrieving, updating, and deleting a blog by ID
    path('<int:pk>/', views.BlogUpdateRetrieveDestroyView.as_view(), name='blog-detail'),
    # Endpoint for creating a new comment
    path('comments/', views.CommentCreateUpdateView.as_view(), name='comment-create'),
    # Endpoint for updating and deleting a specific comment
    path('comments/<int:pk>/', views.CommentCreateUpdateView.as_view(), name='comment-update'),
    # Endpoint for creating and deleting a like for a blog
    path('<int:blog_id>/like/', views.LikeCreateDeleteView.as_view(), name='like-create-delete'),
    # Endpoint for creating and deleting a like for a comment
    path('comments/<int:comment_id>/like/', views.CommentLikeCreateDeleteView.as_view(), name='comment-like-create-delete'),
    # Endpoint for listing all blogs of a specific user
    path('user/<str:username>/', views.UserBlogListAPIView.as_view(), name='user-blog-list'),
    # Endpoint for listing all blogs of self
    path('self/', views.SelfBlogListAPIView.as_view(), name='self-blog-list'),
    # Endpoint for listing all tags
    path('tags/', views.TagListAPIView.as_view(), name='tag-list'),
]

