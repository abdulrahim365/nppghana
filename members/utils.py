from django.conf import settings
from django.core.mail import send_mail


def send_claim_status_email(claim):
    if claim.status not in ("approved", "rejected"):
        return

    if claim.status == "approved":
        subject = "Your NPP claim has been approved"
        body = (
            f"Dear {claim.full_name},\n\n"
            f"Your {claim.claim_type} claim has been approved.\n\n"
            f"Details you submitted:\n{claim.details}\n\n"
            f"Our team may contact you on {claim.phone} or {claim.email}.\n\n"
            f"Thank you.\n"
            f"New Patriotic Party (NPP) Ghana"
        )
    else:
        subject = "Update on your NPP claim"
        body = (
            f"Dear {claim.full_name},\n\n"
            f"Your {claim.claim_type} claim has been reviewed and was not approved at this time.\n\n"
            f"If you have questions, contact us at info@newpatrioticparty.org "
            f"or call +233 30 222 2222.\n\n"
            f"Thank you.\n"
            f"New Patriotic Party (NPP) Ghana"
        )

    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[claim.email],
        fail_silently=False,
    )