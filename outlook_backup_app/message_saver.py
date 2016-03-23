import os
from datetime import datetime
from django.template.defaultfilters import slugify
from base64 import standard_b64decode
from settings import DEFAULT_SAVE_DIR

def save_file(filename, content):
    final_full_path = os.path.join(DEFAULT_SAVE_DIR, filename)
    final_dir_path = os.path.dirname(final_full_path)
    if not os.path.exists(final_dir_path):
        os.makedirs(final_dir_path)
        os.chmod(final_dir_path, 0777)
    with open(final_full_path, mode="w") as the_file:
        the_file.write(content)

def save_attachments(filename_for_the_message, attachment_list):
    attachment_dir = filename_for_the_message.split(".")[0]
    attachment_dir = slugify(attachment_dir)
    if not os.path.exists(attachment_dir):
        os.makedirs(attachment_dir)
        os.chmod(attachment_dir, 0777)
    for attachment in attachment_list:
        filename = attachment["Name"].split(".")
        filename = "{0}.{1}".format(slugify(filename[0]),filename[1])
        file_path = os.path.join(attachment_dir, filename)
        content = standard_b64decode(attachment["ContentBytes"])
        save_file(file_path, content)

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