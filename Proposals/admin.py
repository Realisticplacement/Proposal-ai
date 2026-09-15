from django.contrib import admin
from .models import PricingItem, Proposal, ProposalSection, ProposalLineItem, ProposalVersion

# Register your models here.
admin.site.register(Proposal)
admin.site.register(ProposalSection)
admin.site.register(ProposalLineItem)
admin.site.register(ProposalVersion)
admin.site.register(PricingItem)
