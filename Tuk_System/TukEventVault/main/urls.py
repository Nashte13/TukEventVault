from django.urls import path
from . import views

urlpatterns = [
    # Basic pages
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    
    # User authentication
    path('register/', views.register, name='register'),
    
    # User and admin dashboards
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Event CRUD operations
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),

     path('add_event/', views.add_event, name='add_event'),
    
    # Blog CRUD operations
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blogs/create/', views.create_blog, name='create_blog'),
    path('blogs/<int:blog_id>/edit/', views.edit_blog, name='edit_blog'),
    # Search functionality
    path('search/', views.search_view, name='search'),

    
    # Download functionality
    path('download/<int:event_data_id>/', views.download_event_data, name='download_event_data'),

    path('admin/users/', views.user_list, name='user_list'),
    path('admin/users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('admin/users/<int:user_id>/edit/', views.edit_user, name='edit_user'),

    #gallery functionality
    path('gallery/', views.gallery_list, name='gallery'),  # This will be the main gallery page
    path('gallery/<int:event_id>/', views.gallery_detail, name='gallery_detail'),
    path('gallery/create/<int:event_id>/', views.create_gallery, name='create_gallery'),
    path('gallery/add-item/<int:gallery_id>/', views.add_gallery_item, name='add_gallery_item'),
    path('gallery/download/<int:item_id>/', views.download_gallery_item, name='download_gallery_item'),

    #contact functionality
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('event-submission/', views.event_submission, name='event_submission'),
    path('report-issue/', views.report_issue, name='report_issue'),
 

    #authentication functionalities
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),

    #user profile edit
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

   
]