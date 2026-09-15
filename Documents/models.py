from django.db import models

# Create your models here.
class Document(models.Model):
    class DocumentType(models.TextChoices):
        SITE_WALK = "Site_Walk", "Site Walk"
        PRICING = "Pricing", "Pricing"
        TEMPLATE = "Template", "Template"
        GENERATED_PROPOSAL = "Generated_Proposal", "Generated Proposal"
    organization = models.ForeignKey('Accounts.Organization', on_delete=models.CASCADE, related_name="documents", null=True, blank=True)
    client = models.ForeignKey('Clients.Client', on_delete=models.CASCADE, related_name="documents", null=True, blank=True)
    proposal = models.ForeignKey('Proposals.Proposal', on_delete=models.CASCADE, related_name="documents", null=True, blank=True)
    document_type = models.CharField(max_length=50, choices=DocumentType.choices)
    file = models.FileField(upload_to="documents/%Y/%m/%d/", blank= True, null= True)
    extracted_text = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name