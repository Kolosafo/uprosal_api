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
    path('user_qouta/<str:user_email>', views.get_user_qouta, name="user_qouta"),
    path('reduce_qouta/<str:user_email>', views.reduce_qouta, name="reduce_qouta"),

    path('confirm_email/', views.confirm_email, name="confirm_email"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('password_reset/', views.password_reset, name="password_reset"),
    path('test_email/', views.testEmail, name="test_email"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
