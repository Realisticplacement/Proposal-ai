from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from Clients.models import Client
from .twilio.services import send_client_sms

# Create your views here.



class SendClientSMSView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, client_id):

        client = Client.objects.filter(id=client_id,organization=request.user.organization,).first()

        if not client:

            return Response({"detail": "Client not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not client.phone_number:
            return Response(
                {"detail": "This client does not have a phone number."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        message = request.data.get("message")

        if not message:

            return Response({"detail": "Message is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sms = send_client_sms(client,message,)

        return Response({"status": "sent","message_id": sms.id,"twilio_sid": sms.twilio_message_sid,},
            status=status.HTTP_200_OK,
        )