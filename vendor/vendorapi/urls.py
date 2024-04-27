from django.urls import path
from vendorapi.views import homepage

urlpatterns = [
    path('', homepage, name="api-homepage")
]