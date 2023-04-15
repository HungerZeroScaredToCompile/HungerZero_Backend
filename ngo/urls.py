from django.urls import path
from . import views

urlpatterns = [
    # path('mailtest/',views.mailtest, name='send_mail'),
    
    #url for ngo profile
    path('ngoprofile/',views.UserProfileView.as_view()),
    path('ngoprofile/<str:username>',views.UserProfileView.as_view()),
    #url for stats
    path('statsapi/',views.StatsAPI.as_view()),
    path('statsapi/<int:pk>',views.StatsAPI.as_view()),
    #url for feedback
    path('feedback/',views.FeedbackAPIView.as_view()),
    path('feedback/<int:pk>',views.FeedbackAPIView.as_view()),
    path('feedbackanalysis',views.FBAnalysis)

]
