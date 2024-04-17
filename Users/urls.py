from django.urls import path
from .views import ProfileAvatarView, ProfileView, LogoutView, RegisterView, LoginView,EmailVerification,UpdatePasswordView,ResendVerificationLinkView

urlpatterns = [
    path('login',LoginView.as_view()),
    path('register',RegisterView.as_view()),
    path('logout',LogoutView.as_view()),
    path('profile',ProfileView.as_view()),
    path('password',UpdatePasswordView.as_view()),
    path('resend',ResendVerificationLinkView.as_view()),
    path('activate/<str:token>',EmailVerification.as_view()),
    path('profile/upload-avatar/', ProfileAvatarView.as_view(), name='upload-profile-avatar') #  : API URL
    

]
