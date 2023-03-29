from django.urls import path
from django.views.generic import TemplateView
from . import views

from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


app_name = 'accounts'
urlpatterns = [
    # url path to get posts
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
