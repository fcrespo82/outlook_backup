import os
from datetime import datetime
from django.template.defaultfilters import slugify

DEFAULT_DIR='output'

def save_file(filename, content):
    with open("/".join([DEFAULT_DIR, filename]), mode="w") as the_file:
        the_file.write(content)

def save_attachments(filename_for_the_message, attachment_list):
    attachment_dir = filename_for_the_message.split(".")[0]
    attachment_dir = "/".join([DEFAULT_DIR, attachment_dir])
    if not os.path.exists(attachment_dir):
        os.mkdir(attachment_dir)
    for attachment in attachment_list:
        print(attachment)
        save_file("/".join([attachment_dir, attachment["Name"]]), attachment["Content"])

def save_message(message, content):
    date_string = message['ReceivedDateTime']
    subject = message['Subject']
    subject = slugify(subject)

    date_format = "%Y-%m-%dT%H:%M:%SZ"
    date_format_string = "%Y_%m_%d-%H_%M_%S"

    date = datetime.strptime(date_string, date_format)
    date_string = date.strftime(date_format_string)
    filename = u"{0}-{1}.html".format(date_string, subject)
    save_file(filename, content)