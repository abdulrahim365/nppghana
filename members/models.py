from django.db import models


class MembershipApplication(models.Model):
    title = models.CharField(max_length=20, blank=True)
    surname = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=150, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    residential_address = models.TextField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    hometown = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100, blank=True)
    voter_id = models.CharField(max_length=50, blank=True)
    polling_station = models.CharField(max_length=150, blank=True)
    constituency = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.surname}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Donation(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    donor_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor_name} - GHS {self.amount}"


class DuesPayment(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
    )
    TIER_CHOICES = (
        ("Bronze", "Bronze"),
        ("Gold", "Gold"),
        ("Silver", "Silver"),
        ("Diamond", "Diamond"),
    )

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.tier} - GHS {self.amount}"


class Claim(models.Model):
    STATUS_CHOICES = (
        ("submitted", "Submitted"),
        ("reviewing", "Under Review"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )
    TYPE_CHOICES = (
        ("Funeral", "Funeral"),
        ("Medical", "Medical"),
        ("Other", "Other"),
    )

    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    membership_id = models.CharField(max_length=50, blank=True)
    claim_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    details = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="submitted")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.claim_type}"