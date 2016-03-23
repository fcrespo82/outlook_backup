from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from outlook_backup_app.authhelper import get_signin_url, get_token_from_code, get_user_email_from_id_token
from outlook_backup_app.outlookservice import get_my_messages, get_message, get_message_attachments, get_attachment
from settings import DEFAULT_SAVE_DIR, SITE_ROOT
from outlook_backup_app.message_saver import save_message, save_attachments
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify

import urlparse
import urllib
import json
import os

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
        next_link=request.META['QUERY_STRING']
        previous_link=""
        if request.META['QUERY_STRING']:
            parameters = urlparse.parse_qs(request.META['QUERY_STRING'])
            messages = get_my_messages(access_token, user_email, parameters)
            previous_parameter = parameters
            previous_parameter['$select'] = previous_parameter['$select'][0]
            previous_parameter['$orderby'] = previous_parameter['$orderby'][0]
            previous_parameter['$top'] = previous_parameter['$top'][0]
            previous_parameter['$skip'] = str(int(previous_parameter['$skip'][0]) - 10)
            if int(previous_parameter['$skip']) >= 0:
                previous_link = urllib.urlencode(previous_parameter)
        else:
            messages = get_my_messages(access_token, user_email)
        if messages.has_key('@odata.nextLink'):
            next_link = urlparse.urlparse(messages['@odata.nextLink']).query

        context = { 'messages': messages['value'], 'next_link': next_link, 'previous_link': previous_link }
        return render(request, 'outlook_backup_app/mail.html', context)
    
def preview(request):
    access_token = request.session['access_token']
    user_email = request.session['user_email']

    message_id = request.GET['message_id']
    
    message = get_message(access_token, user_email, message_id)
    
    attachments = get_message_attachments(access_token, user_email, message_id)
    
    att_contents = []
    
    for attachment in attachments:
        filename = attachment["Name"].split(".")
        filename = "{0}.{1}".format(slugify(filename[0]),filename[1])
        attachment.update({"filename": filename})
        att_content = get_attachment(access_token, user_email, message_id, attachment['Id'])
        att_contents.append(att_content)
    
    relative_path = os.path.relpath(DEFAULT_SAVE_DIR, SITE_ROOT)

    context = { 'message': message, 'attachments': attachments, 'saved_path': relative_path }
    
    response = render(request, 'outlook_backup_app/preview.html', context)
    
    save_message(message, response.content)
    
    if attachments:
        save_attachments(message['Subject'], att_contents)
    
    return response

