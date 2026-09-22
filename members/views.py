import hashlib
import hmac
import json
import uuid

import requests
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import (
    Claim,
    Donation,
    DuesPayment,
    MembershipApplication,
    NewsletterSubscriber,
)


TIERS = {
    "Bronze": 2,
    "Gold": 5,
    "Silver": 8,
    "Diamond": 10,
}


def join_view(request):
    if request.method == "POST":
        MembershipApplication.objects.create(
            title=request.POST.get("title"),
            surname=request.POST.get("surname"),
            first_name=request.POST.get("first_name"),
            other_names=request.POST.get("other_names"),
            gender=request.POST.get("gender"),
            date_of_birth=request.POST.get("date_of_birth") or None,
            residential_address=request.POST.get("residential_address"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            hometown=request.POST.get("hometown"),
            region=request.POST.get("region"),
            occupation=request.POST.get("occupation"),
            voter_id=request.POST.get("voter_id"),
            polling_station=request.POST.get("polling_station"),
            constituency=request.POST.get("constituency"),
        )
        messages.success(
            request,
            "Your membership application has been submitted successfully!",
        )
        return redirect("members:join")
    return render(request, "members/join.html")


def donate_view(request):
    return render(request, "members/donate.html")


def initiate_payment(request):
    if request.method != "POST":
        return JsonResponse({"status": False, "message": "Invalid method"})

    name = request.POST.get("donor_name", "").strip()
    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()
    amount = request.POST.get("amount")

    if not name or not email or not amount:
        return JsonResponse({"status": False, "message": "Missing fields"})

    try:
        amount_val = float(amount)
        if amount_val <= 0:
            raise ValueError()
    except ValueError:
        return JsonResponse({"status": False, "message": "Invalid amount"})

    reference = f"DON-{uuid.uuid4().hex[:12].upper()}"

    Donation.objects.create(
        donor_name=name,
        email=email,
        phone=phone,
        amount=amount_val,
        reference=reference,
        status="pending",
    )

    return JsonResponse(
        {
            "status": True,
            "public_key": settings.PAYSTACK_PUBLIC_KEY,
            "email": email,
            "amount": int(amount_val * 100),
            "reference": reference,
            "name": name,
        }
    )


def verify_payment(request):
    reference = request.GET.get("reference")
    if not reference:
        messages.error(request, "No payment reference found.")
        return redirect("members:donate")

    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    result = requests.get(url, headers=headers).json()

    try:
        donation = Donation.objects.get(reference=reference)
    except Donation.DoesNotExist:
        messages.error(request, "Donation record not found.")
        return redirect("members:donate")

    if result.get("status") and result.get("data", {}).get("status") == "success":
        donation.status = "success"
        donation.save()
        return render(
            request,
            "members/donate_success.html",
            {"donation": donation},
        )

    donation.status = "failed"
    donation.save()
    messages.error(request, "Payment verification failed.")
    return redirect("members:donate")


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            NewsletterSubscriber.objects.get_or_create(email=email)
            return JsonResponse(
                {"success": True, "message": "Subscribed successfully!"}
            )
    return JsonResponse({"success": False})


def pay_dues(request):
    return render(
        request,
        "members/pay_dues.html",
        {
            "tiers": [
                {"name": "Bronze", "amount": 2},
                {"name": "Gold", "amount": 5},
                {"name": "Silver", "amount": 8},
                {"name": "Diamond", "amount": 10},
            ],
        },
    )


def initiate_dues_payment(request):
    if request.method != "POST":
        return JsonResponse({"status": False, "message": "Invalid method"})

    tier = request.POST.get("tier")
    name = request.POST.get("full_name", "").strip()
    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()

    if tier not in TIERS:
        return JsonResponse({"status": False, "message": "Invalid tier"})
    if not name or not email:
        return JsonResponse({"status": False, "message": "Name and email required"})

    amount = TIERS[tier]
    reference = f"DUES-{uuid.uuid4().hex[:12].upper()}"

    DuesPayment.objects.create(
        full_name=name,
        email=email,
        phone=phone,
        tier=tier,
        amount=amount,
        reference=reference,
        status="pending",
    )

    return JsonResponse(
        {
            "status": True,
            "public_key": settings.PAYSTACK_PUBLIC_KEY,
            "email": email,
            "amount": int(float(amount) * 100),
            "reference": reference,
            "name": name,
            "tier": tier,
        }
    )


def verify_dues_payment(request):
    reference = request.GET.get("reference")
    if not reference:
        messages.error(request, "No payment reference found.")
        return redirect("members:pay_dues")

    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    result = requests.get(url, headers=headers).json()

    try:
        payment = DuesPayment.objects.get(reference=reference)
    except DuesPayment.DoesNotExist:
        messages.error(request, "Dues record not found.")
        return redirect("members:pay_dues")

    if result.get("status") and result.get("data", {}).get("status") == "success":
        payment.status = "success"
        payment.save()
        return render(
            request,
            "members/dues_success.html",
            {"payment": payment},
        )

    payment.status = "failed"
    payment.save()
    messages.error(request, "Payment verification failed.")
    return redirect("members:pay_dues")


@csrf_exempt
@require_POST
def paystack_webhook(request):
    payload = request.body
    signature = request.META.get("HTTP_X_PAYSTACK_SIGNATURE", "")

    secret = settings.PAYSTACK_SECRET_KEY.encode("utf-8")
    computed = hmac.new(secret, payload, hashlib.sha512).hexdigest()

    if not hmac.compare_digest(computed, signature):
        return JsonResponse({"status": "invalid signature"}, status=400)

    try:
        event = json.loads(payload.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"status": "invalid payload"}, status=400)

    event_type = event.get("event")
    data = event.get("data") or {}
    reference = data.get("reference")

    if event_type == "charge.success" and reference:
        try:
            dues = DuesPayment.objects.get(reference=reference)
            dues.status = "success"
            dues.save(update_fields=["status"])
        except DuesPayment.DoesNotExist:
            pass

        try:
            donation = Donation.objects.get(reference=reference)
            donation.status = "success"
            donation.save(update_fields=["status"])
        except Donation.DoesNotExist:
            pass

    elif event_type in ("charge.failed", "transfer.failed") and reference:
        DuesPayment.objects.filter(reference=reference).update(status="failed")
        Donation.objects.filter(reference=reference).update(status="failed")

    return JsonResponse({"status": "ok"}, status=200)


def claims_view(request):
    if request.method == "POST":
        Claim.objects.create(
            full_name=request.POST.get("full_name", "").strip(),
            email=request.POST.get("email", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            membership_id=request.POST.get("membership_id", "").strip(),
            claim_type=request.POST.get("claim_type"),
            details=request.POST.get("details", "").strip(),
        )
        messages.success(
            request,
            "Your claim has been submitted successfully. Our team will review it and contact you.",
        )
        return redirect("members:claims")

    return render(request, "members/claims.html")