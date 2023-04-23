from django.urls import path
from users import views

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path("login/",views.JWTLogin.as_view(),name="login"),
    path("<int:user_id>/logout/",views.LogOutView.as_view(),name="logout"),

    path("check/", views.CheckView.as_view(), name="check"),

    path('api/token/', views.CustomTokenObtainPariView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    

]