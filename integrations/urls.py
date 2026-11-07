from django.urls import path

from .views import AvatarScenesView, SoapCapitalView


urlpatterns = [
    path('avatar-scenes/', AvatarScenesView.as_view(), name='avatar-scenes'),
    path('soap/capital/', SoapCapitalView.as_view(), name='soap-capital'),
]
