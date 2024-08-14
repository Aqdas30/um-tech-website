
from urllib import response
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework.response import Response

from .forms import ContactForm
from .models import Service
from .serializers import ServiceSerializer
from django.core.mail import send_mail
def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            service_type = form.cleaned_data['service_type']

            service = Service.objects.get(id=service_type)
            service_name = service.title

            send_mail(
                subject=f'Contact Form Submission from {name}',
                message=f'Phone Number: {phone_number}\nEmail: {email}\nService Type: {service_name}\nMessage: {message}',
                from_email=email,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )

            return JsonResponse({
                'status': 'success',
                'message': f'Thank You. Your request for the {service_name} service has been received. Our team will contact you shortly.'
            })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = ContactForm()

    return render(request, 'index.html', {'form': form})


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceListPreviewView(generics.ListAPIView):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        return Service.objects.all()[:3]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
