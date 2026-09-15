from django.urls import path
from.views import SendClientSMSView
from .twilio.webhook import incoming_sms

urlpatterns = [
     path("clients/<int:client_id>/sms/",SendClientSMSView.as_view(),name="send-client-sms",),
     path("twilio/webhook/",incoming_sms,name="twilio-webhook",)
]