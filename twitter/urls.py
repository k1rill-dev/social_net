from django.urls import path, re_path
from .views import *



urlpatterns = [
    path('', PostView.as_view(), name='posts'),
    path('register/', register, name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('red/', red, name='redirect_to_login'),
    path('profile_edit/', profile, name='profile_edit'),
    path('profile/<int:pk>', DetailUserView.as_view(), name='user_profile'),
    path('post/<int:pk>/', post_view, name='detail_post_view'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('logout/', logout_user, name='logout_user'),
    path('user/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('user/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
    path('like/add/', AddLikeView.as_view(), name='add_like'),
    path('like/remove/', RemoveLikeView.as_view(), name='remove_like'),
    # path('like/add-ajax/', add_like_ajax, name='add_like_ajax'),
    # path('like/remove-ajax/', remove_like_ajax, name='remove_like_ajax'),
    path('api/search/', api_search_query_view, name='api_search'),
    path('api/search_query/?q=<str:q>', api_search_query_view_with_q, name='api_search_query'),
    path('api/like-info/<int:post_id>', api_post_like_info, name='api_like_info'),
]