from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

auth_patterns = [
    path("email/", views.send_email),
    path("token/", views.RegisterView.as_view()),
]

router = DefaultRouter()

router.register(r"", views.AllUserViewSet, basename="users")


urlpatterns = [
    # Router endpoints
    path("auth/", include(auth_patterns)),
    path("users/", include(router.urls)),
]
