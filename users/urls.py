from django.urls import path, re_path
from dj_rest_auth import views as auth_views
from dj_rest_auth.registration import views as reg_views


# can't namespace these because of how 
# dj_rest_auth works: need to reverse account_confirm_email
urlpatterns = [
	path("signup/", reg_views.RegisterView.as_view(), name= "signup"),
	path("login/", auth_views.LoginView.as_view(), name= "login"),
	path("logout/", auth_views.LogoutView.as_view(), name= "logout"),
	
	path("user/", auth_views.UserDetailsView.as_view(), name= "user"),

	path("password/change/", auth_views.PasswordChangeView.as_view(), name= "change_password"),
    
	# here for reversal purposes
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', reg_views.VerifyEmailView.as_view(), name= "account_confirm_email"),
]