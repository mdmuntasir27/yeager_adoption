from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='community_home'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/mark-given/', views.mark_given, name='mark_given'),
    path('post/<int:pk>/inquire/', views.submit_inquiry, name='submit_inquiry'),
    path('post/<int:pk>/inquiries/', views.post_inquiries, name='post_inquiries'),
    path('inquiry/<int:inquiry_pk>/update-status/', views.update_inquiry_status, name='update_inquiry_status'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('my-inquiries/', views.my_inquiries, name='my_inquiries'),
    path('user/<str:username>/', views.public_profile, name='public_profile'),
]

