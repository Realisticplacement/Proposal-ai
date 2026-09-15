from django.conf import settings

from Integrations.models import SMSMessage

from .client import twilio_client


def send_client_sms(client,message,):

    if not client.phone_number:
        raise ValueError("The client must have a phone number before sending SMS.")

    sms = SMSMessage.objects.create(
        organization=client.organization,
        client=client,
        direction=SMSMessage.Direction.OUTGOING,
        phone_number=client.phone_number,
        message=message,
        status=SMSMessage.Status.QUEUED,
    )

    try:

        response = twilio_client.messages.create(body=message,from_=settings.TWILIO_PHONE_NUMBER, to=client.phone_number,)

        sms.twilio_message_sid = response.sid

        sms.status = SMSMessage.Status.SENT

        sms.save(update_fields=["twilio_message_sid","status","updated_at",])

        return sms

    except Exception:

        sms.status = SMSMessage.Status.FAILED

        sms.save(update_fields=["status","updated_at",])

        raise