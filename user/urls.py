from django.urls import path, include
from user import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', views.UserViewSet, basename='user_registrations')
router.register(r'discussion', views.DiscussionViewSet, basename='user_discussion')

urlpatterns = [
    path('', include(router.urls)),
]