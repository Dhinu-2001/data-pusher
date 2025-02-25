from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'account', views.AccountViewSet)
router.register(r'destination', views.DestinationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register_user),
    path('server/incoming_data/', views.incoming_data),
    path('api-token-auth/', views.CustomAuthToken.as_view()),
    path('logout/', views.logout_user),
]
