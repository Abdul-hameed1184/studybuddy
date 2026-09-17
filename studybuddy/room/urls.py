from django.urls import path, include

from . import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.home, name='home'),
    path('room/create/', views.create_room_view, name='create-room'),
    path('room/<slug:slug>/', views.room_detail, name='room-detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path(
        "auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "auth/user/register", views.createUserView.as_view(), name='register_api'
    ),
    path(
        "api-auth/", include("rest_framework.urls")
    ),
    path("messages/", views.messageListCreate.as_view(), name='message'),
    path("rooms/", views.roomListCreate.as_view(), name='rooms'),
]
