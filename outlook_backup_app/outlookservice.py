import requests
import uuid
import json

outlook_api_endpoint = 'https://outlook.office.com/api/v2.0{0}'

# Generic API Sending
def make_api_call(method, url, token, user_email, payload = None, parameters = None):
    # Send these headers with all API calls
    headers = { 'User-Agent' : 'outlook_backup_app/1.0',
                'Authorization' : 'Bearer {0}'.format(token),
                'Accept' : 'application/json',
                'X-AnchorMailbox' : user_email }

    # Use these headers to instrument calls. Makes it easier
    # to correlate requests and responses in case of problems
    # and is a recommended best practice.
    request_id = str(uuid.uuid4())
    instrumentation = { 'client-request-id' : request_id,
                        'return-client-request-id' : 'true' }

    headers.update(instrumentation)

    response = None

    if (method.upper() == 'GET'):
        response = requests.get(url, headers = headers, params = parameters)
    elif (method.upper() == 'DELETE'):
        response = requests.delete(url, headers = headers, params = parameters)
    elif (method.upper() == 'PATCH'):
        headers.update({ 'Content-Type' : 'application/json' })
        response = requests.patch(url, headers = headers, data = json.dumps(payload), params = parameters)
    elif (method.upper() == 'POST'):
        headers.update({ 'Content-Type' : 'application/json' })
        response = requests.post(url, headers = headers, data = json.dumps(payload), params = parameters)

    return response
    
def get_my_messages(access_token, user_email):
    #get_messages_url = outlook_api_endpoint.format('/Me/Messages')
    get_messages_url = outlook_api_endpoint.format('/me/mailfolders/inbox/messages')
    # Use OData query parameters to control the results
    #  - Only first 10 results returned
    #  - Only return the ReceivedDateTime, Subject, and From fields
    #  - Sort the results by the ReceivedDateTime field in descending order
    query_parameters = {'$top': '100',
                        '$select': 'ReceivedDateTime,Subject,From,HasAttachments',
                        '$orderby': 'ReceivedDateTime DESC'}

    r = make_api_call('GET', get_messages_url, access_token, user_email, parameters = query_parameters)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)
        
def get_message(access_token, user_email, message_id):
    #get_messages_url = outlook_api_endpoint.format('/Me/Messages')
    get_message_url = outlook_api_endpoint.format('/me/messages/{message_id}'.format(message_id=message_id))
    # Use OData query parameters to control the results

    #query_parameters = {'$select': 'ReceivedDateTime,Subject,From',
                        #'$orderby': 'ReceivedDateTime DESC'}

    r = make_api_call('GET', get_message_url, access_token, user_email)#, parameters = query_parameters)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)
        
def get_message_attachments(access_token, user_email, message_id):
    get_attachments_url = outlook_api_endpoint.format('/me/messages/{message_id}/attachments'.format(message_id=message_id))
    r = make_api_call('GET', get_attachments_url, access_token, user_email)
    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)
