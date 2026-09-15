from django.db import models

# Create your models here.
class AIExecution(models.Model):
    class AgentType(models.TextChoices):
        PROPOSAL = 'proposal', 'Proposal Agent'
        REVIEW = 'review', 'Proposal Review'
        EXTRACTION = 'extraction', 'Document Extraction'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        RUNNING = 'running', 'Running'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    organization = models.ForeignKey('Accounts.Organization', on_delete=models.CASCADE, related_name="ai_executions", null=True, blank=True)    
    agent_type = models.CharField(max_length=50, choices=AgentType.choices)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)
    proposal = models.ForeignKey('Proposals.Proposal', on_delete=models.CASCADE, related_name="ai_executions", null=True, blank=True)
    input_data = models.JSONField(default=dict, blank=True)
    output_data = models.JSONField(default=dict, blank=True)
    model_name = models.CharField(max_length=100, blank=True, null=True)
    token_used = models.PositiveIntegerField(null=True, blank=True)
    output_token = models.PositiveIntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null= True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
