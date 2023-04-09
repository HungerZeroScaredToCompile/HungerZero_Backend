from django.urls import path
from .views import VolunteerListCreateAPIView,ListAllNotificationView,ContactUsView,DonationListCreateView,CreateNotificationTimeView,UserProfileView,DonationBy,NgoDonationStats,ListNotificationView,CreateNotificationView,CommunityPosts
app_name = 'volunteers','donations','contact_us'

urlpatterns = [
    path('volunteers/', VolunteerListCreateAPIView.as_view(), name='volunteer_list_create'),
    path('donations/', DonationListCreateView.as_view(), name='donation_list-create'),
    path('donations/group_by_ngo/', DonationListCreateView.as_view(), {'group_by_ngo': True}, name='donation_list_by_ngo'),
    path('donations/stats/<str:ngo>/', NgoDonationStats.as_view(), name='ngo_donation_stats'),
    path('donations/by/', DonationBy.as_view(), name='donation_by'),
    # path('users/notifications/<str:username>/', UserNotificationView.as_view(), name='user_notifications'),
    path('notifications/create/', CreateNotificationView.as_view(), name='create_notification'),
    path('notifications/create/default/', CreateNotificationTimeView.as_view(), name='create_default_notification'),
    path('notifications/list/', ListAllNotificationView.as_view(), name='notifications-list'),
    path('notifications/<str:username>/', ListNotificationView.as_view(), name='notifications-list-user'),
    path('api/users/<str:username>', UserProfileView.as_view(), name='user_profile'),
    path('communities/', CommunityPosts.as_view(), name='community-list-create'),
    path('contact_us/', ContactUsView.as_view(), name='contact_us'),

]










