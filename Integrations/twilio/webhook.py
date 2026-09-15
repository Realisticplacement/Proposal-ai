from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.request_validator import RequestValidator

from twilio.twiml.messaging_response import (MessagingResponse)


@csrf_exempt
def incoming_sms(request):

    if request.method != "POST":

        return HttpResponse(status=405)

    signature = request.headers.get("X-Twilio-Signature")
    auth_token = settings.TWILIO_AUTH_TOKEN
    if not signature or not auth_token:
        return HttpResponse(status=403)

    validator = RequestValidator(auth_token)
    if not validator.validate(
        request.build_absolute_uri(),
        request.POST,
        signature,
    ):
        return HttpResponse(status=403)

    response = MessagingResponse()

    response.message("Thanks! We've received your message.")

    return HttpResponse(str(response),content_type="text/xml")