from django.urls import path

from .views import CartValidateView

urlpatterns = [
    path("validate/", CartValidateView.as_view(), name="cart-validate"),
]
