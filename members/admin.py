from django.contrib import admin

from django.contrib import admin, messages
from .models import Claim
from .utils import send_claim_status_email
from .models import (
    MembershipApplication,
    NewsletterSubscriber,
    Donation,
    DuesPayment,
    Claim,
)


@admin.register(MembershipApplication)
class MembershipApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "full_name_display",
        "email",
        "phone",
        "region",
        "constituency",
        "created_at",
    )
    list_filter = ("region", "gender", "created_at")
    search_fields = ("first_name", "surname", "email", "phone", "constituency")
    readonly_fields = ("created_at",)

    def full_name_display(self, obj):
        return f"{obj.title} {obj.first_name} {obj.surname}".strip()

    full_name_display.short_description = "Full Name"


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "subscribed_at")
    search_fields = ("email",)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("donor_name", "email", "amount", "status", "reference", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("donor_name", "email", "reference")


@admin.register(DuesPayment)
class DuesPaymentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "tier", "amount", "status", "reference", "created_at")
    list_filter = ("tier", "status", "created_at")
    search_fields = ("full_name", "email", "phone", "reference")




@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ("full_name", "claim_type", "phone", "status", "created_at")
    list_filter = ("claim_type", "status", "created_at")
    search_fields = ("full_name", "email", "phone", "membership_id")
    list_editable = ("status",)
    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):
        old_status = None
        if change and obj.pk:
            old_status = Claim.objects.filter(pk=obj.pk).values_list("status", flat=True).first()

        super().save_model(request, obj, form, change)

        if obj.status in ("approved", "rejected") and obj.status != old_status:
            try:
                send_claim_status_email(obj)
                messages.success(request, f"Notification email sent to {obj.email}.")
            except Exception as e:
                messages.warning(request, f"Claim saved, but email failed: {e}")