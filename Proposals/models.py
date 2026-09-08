from django.db import models
from Accounts.models import Organization, User

# Create your models here.
class Proposal(models.Model):
    class Status(models.TextChoices):
        SITE_WALK_DATA = 'Site Walk Data', 'Site Walk Data'
        PROSSING = 'Processing', 'Processing'
        DRAFT = 'Draft', 'Draft'
        REVIEW = 'Review', 'Review'
        CHANGES_REQUESTED = 'Changes Requested', 'Changes Requested'
        APPORVED = 'Approved', 'Approved'
        SENT = 'Sent', 'Sent'

    organization = models.ForeignKey('Accounts.Organization', on_delete=models.CASCADE, related_name="proposals", null=True, blank=True)
    client = models.ForeignKey('Clients.Client', on_delete=models.CASCADE, related_name="proposals", null=True, blank=True)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.SITE_WALK_DATA)
    note = models.TextField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_by = models.ForeignKey('Accounts.User', on_delete=models.SET_NULL, related_name="created_proposals", null=True, blank=True)
    apporved_by = models.ForeignKey('Accounts.User', on_delete=models.SET_NULL, related_name="approved_proposals", null=True, blank=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class ProposalSection(models.Model):
    proposal = models.ForeignKey('Proposal', on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
    


class ProposalLineItem(models.Model):
    proposal = models.ForeignKey('Proposal', on_delete=models.CASCADE, related_name="line_items")
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit = models.CharField(max_length=50, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    source_reference = models.CharField(max_length=255, blank=True, null=True)
    ai_suggested = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProposalVersion(models.Model):
    proposal = models.ForeignKey('Proposal', on_delete=models.CASCADE, related_name="versions")
    version_number = models.PositiveIntegerField()
    content = models.JSONField()
    created_by = models.ForeignKey('Accounts.User', on_delete=models.SET_NULL, related_name="created_proposal_versions", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-version_number']
        constraints = [
            models.UniqueConstraint(fields=['proposal', 'version_number'], name='unique_proposal_version')
        ]
