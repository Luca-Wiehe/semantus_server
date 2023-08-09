"""
URLs define API endpoints that are available to users. They redirect sent requests to the respective views,
obtain a response and send this response back to the person who sent the request.
"""

from django.urls import path
from .views import HomepageView, SignupView, LoginView, UsernameCheckView

urlpatterns = [
    path("", HomepageView.as_view(), name="homepage-view"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("check-username/", UsernameCheckView.as_view(), name="check-username"),
    path("login/", LoginView.as_view(), name="login"),
]
