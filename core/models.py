from django.db import models

class Leader(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='leaders/')
    is_flagbearer = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Achievement(models.Model):
    title = models.CharField(max_length=300)
    short_desc = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('education', 'Education'), ('health', 'Health'),
        ('infrastructure', 'Infrastructure'), ('economy', 'Economy'),
        ('digital', 'Digital Ghana')
    ])
    year = models.IntegerField()
    image = models.ImageField(upload_to='achievements/')

    def __str__(self):
        return self.title

class Timeline(models.Model):
    year = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['year']




class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact message"
        verbose_name_plural = "Contact messages"

    def __str__(self):
        return f"{self.name} — {self.subject}"