from django.db import models

# Create your models here.
class SMSMessage(models.Model):

    class Direction(models.TextChoices):
        INCOMING = 'incoming', 'Incoming'
        OUTGOING = 'outgoing', 'Outgoing'

    class Status(models.TextChoices):
        QUEUED = 'queued', 'Queued'
        SENT = 'sent', 'Sent'
        DELIVERED = 'delivered', 'Delivered'
        FAILED = 'failed', 'Failed'

    id = models.BigAutoField(primary_key=True)
    organization = models.ForeignKey('Accounts.Organization', on_delete=models.CASCADE, related_name="sms_messages", null=True, blank=True)
    client = models.ForeignKey('Clients.Client', on_delete=models.CASCADE, related_name="sms_messages", null=True, blank=True)
    direction = models.CharField(max_length=255, choices=Direction.choices)
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    twilio_message_sid = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, choices=Status.choices, default=Status.QUEUED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone_number} - {self.status}"