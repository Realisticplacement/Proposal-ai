from django.db import models

# Create your models here.

class Client(models.Model):
    class Status(models.TextChoices):
        LEAD = 'lead', 'Lead'
        QUALIFIED = 'Qualified', 'Qualified'
        PROPOSAL = 'proposal', 'Proposal'
        WON = 'won', 'Won'
        LOST = 'lost', 'Lost'

    organization = models.ForeignKey('Accounts.Organization', on_delete=models.CASCADE, related_name="clients", null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.LEAD)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()