from django.urls import path
from . import views

app_name = "members"

urlpatterns = [
    path("join/", views.join_view, name="join"),
    path("donate/", views.donate_view, name="donate"),
    path("donate/initiate/", views.initiate_payment, name="initiate_payment"),
    path("donate/verify/", views.verify_payment, name="verify_payment"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("pay-dues/", views.pay_dues, name="pay_dues"),
    path("pay-dues/initiate/", views.initiate_dues_payment, name="initiate_dues"),
    path("pay-dues/verify/", views.verify_dues_payment, name="verify_dues"),
    path("paystack/webhook/", views.paystack_webhook, name="paystack_webhook"),
    path("claims/", views.claims_view, name="claims"),
]