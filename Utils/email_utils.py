from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.core import signing
from rest_framework_simplejwt.tokens import RefreshToken
import jwt


def send_activation_link(user,request):
     
     token = signing.dumps(user.id)
     activation_link = settings.BACKEND_HOST+"/auth/activate/"+token
    
     subject = "Welcome to our APP!"
     from_email = ''
     #' <donotreply@.com>' #abess
     message='Click the link below to activate your account: ' + activation_link
     recipient_list = [user.email]
     send_mail(
          subject,
          message,
          from_email,
          recipient_list,
          
          html_message=render_to_string('accountActivationTemplate.html',
                                        {'user': user,
                                         'link': activation_link 
                                        }) 
          )

def generate_token(user):
    token = {
        'user': user.id,
        'organisation': user.organisation.id,
        'role': user.role
    }
    return token
