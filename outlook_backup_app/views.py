from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from outlook_backup_app.authhelper import get_signin_url, get_token_from_code, get_user_email_from_id_token
from outlook_backup_app.outlookservice import get_my_messages, get_message, get_message_attachments

from outlook_backup_app.message_saver import save_message
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

def home(request):
    redirect_uri = request.build_absolute_uri(reverse('outlook_backup_app:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')

def gettoken(request):
    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('outlook_backup_app:gettoken'))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']
    user_email = 'email'#get_user_email_from_id_token(token['id_token'])

    # Save the token in the session
    request.session['access_token'] = access_token
    request.session['user_email'] = user_email
    #return HttpResponse('User Email: {0}, Access token: {1}'.format(user_email, access_token))
    return HttpResponseRedirect(reverse('outlook_backup_app:mail'))
  
def mail(request):
    access_token = request.session['access_token']
    user_email = request.session['user_email']
    # If there is no token in the session, redirect to home
    if not access_token:
        return HttpResponseRedirect(reverse('outlook_backup_app:home'))
    else:
        messages = get_my_messages(access_token, user_email)
        context = { 'messages': messages['value'] }
        return render(request, 'outlook_backup_app/mail.html', context)
    
def preview(request):
    access_token = request.session['access_token']
    user_email = request.session['user_email']

    message_id = request.GET['message_id']
    
    message = get_message(access_token, user_email, message_id)
    
    attachments = get_message_attachments(access_token, user_email, message_id)
    
    #return HttpResponse("Message: {0}".format(message))
    context = { 'message': message, 'attachments': attachments }
    
    
    
    response = render(request, 'outlook_backup_app/preview.html', context)
    
    save_message(message, response.content)
    
    return response

