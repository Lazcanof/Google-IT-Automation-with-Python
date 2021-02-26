#!/usr/bin/env python3
import os, sys
from PIL import Image
user = os.getenv('USER') # To get the username from enviroment variable
image_directory = "/home/{}/supplier-data/images/".format(user)
for image_name in os.listdir(image_directory):
    if not image_name.startswith('.') and 'tiff' in image_name:
        image_path = image_directory + image_name
        path = os.path.splitext(image_path)[0]
        im = Image.open(image_path)
        new_path = '{}.jpeg'.format(path)
        im.convert('RGB').resize((600,400)).save(new_path, "JPEG")
#-------------Supplier_image_upload.py-----------------------

#!/usr/bin/env python3
import requests, os
# The url to upload the images
url = "http://localhost/upload/"
#To get the username from enviroment variable
USER = os.getenv('USER')
#The directory wich contains all the images.
image_directory = "/home/{}/supplier-data/images/".format(USER)
# Listin all the files in images directory
files = os.listdir(image_directory)
#Parsing through all the images
for image_name in files:
    # Accepting files that has jpeg extension and ignoring hidden files
    if not image_name.startswith('.') and 'jpeg' in image_name:
        # creating absolute path each image
        image_path = image_directory + image_name
        # uploading jpeg files
        with open(image_path, 'rb') as opened:
            r = requests.post(url, files={'file':opened})

#----------------------run.py(upload information-----------------------------------

#! /usr/bin/env python3
import os
import requests, json

def catalog_data(url,description_dir):
    """ This function will return a list of dictionaries with the detail like name, weight, description, image_name.
    It will change the weight to integer format.
    """
    fruit={}
    for item in os.listdir(description_dir):
        fruit.clear
        filename = os.path.join(description_dir, item)
        with open(filename) as f:
            line = f.readlines()
            description = ""
            for i in range(2, len(line)):
                description = description + line[i].strip('\n').replace(u'\xa0',u'')
            fruit["description"]= description
            fruit["weight"] = int(line[1].strip('\n').strip('lbs'))
            fruit["name"] = line[0].strip('\n')
            fruit["image_name"] = (item.strip('.txt')) + '.jpeg'
            print(fruit)
            if url!="":
                response = requests.post(url, json=fruit)
                print(response.request.url)
                print(response.status_code)
    return 0

if __name__=='__main__':
    url = 'http://localhost/fruits/'
    user = os.getenv('USER')
    description_directory = "/home/{}/supplier-data/descriptions/".format(user)
    catalog_data(url, description_directory)

#---------------------reports.py--------------------------------

#! /usr/bin/env python3
from reportlab.platypus import Paragraph, Spacer, Image, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(file, title, info):
    styles = getSampleStyleSheet()
    report = SimpleDocTemplate(file)
    report_title = Paragraph(title, styles['h1'])
    report_info = Paragraph(add_info, styles['BodyText'])
    empty_line = Spacer(1,20)

    report.build([report_title, empty_line, report_info, empty_line])

#-----------------------------reports_emails-------------

#! /usr/bin/env python3
import datetime
import emails
import os

from run import catalog_data
from reports import generate_report
from emails import generate_email, send_email

def pdf_body(input_for,desc_dir):
    """ Generating a summary with two lists, wich gives the output name and weight"""
    res = []
    wt = []
    for item in os.listdir(desc_dir):
        filename = os.path.join(desc_dir,item)
        with open(filename) as f:
            line = f.readlines()
            weight = line[1].strip('\n')
            name = line[0].strip('\n')
            print(name, weight)
            res.append('name: ' +name)
            wt.append('weight: ' +weight)
            print(res)
            print(wt)
    new_obj = "" #initializing the object 
    #calling values from two list one by one.
    for i in range(len(res)):
        if res[i] and input_for =='pdf':
            new_obj += res[i] +'<br/>'+ wt[i] +'<br/>'+'<br/>'
    return new_obj

if __name__== '__main__':
    user = os.getenv('USER')
    description_directory = '/home/{}/supplier-data/descriptions/'.format(user)  # the directory
    current_date = datetime.date.today().strftime("%B %d, %Y")# creating data in format "may 5, 2020"
    title = 'Processed Update on ' + str(current_date) #Ttle for the PDF
    generate_report('/tmp/processed.pdf', title, pdf_body('pdf', description_directory)) # calling 
    email_subject = 'Upload Completed - Online Fruit Store' #Subject line gice assignament
    email_body = 'All fruit are uploaded to our website successfully. A detailed list is attached to this email'
    msg = generate_email("automation@example.com","student-00-2cc059e36747@example.com".format(user), email_subject, email_body, "/tmp/processed.pdf")
    send_email(msg)

#----------emails.py----------------

#!/usr/bin/env python3

import email
import mimetypes
import smtplib
import os
def generate_email(sender, recipient, subject, body, attachment_path):
  """Creates an email with an attachement."""
  #basic Email formating
  message = email.message.EmailMessage()
  message["From"] = sender
  message["To"] = recipient
  message["Subject"] = subject
  message.set_content(body)
  #making attachement_path optional, if attachement variable is empty string
  if not attachment_path == "":
    #Process the attachement and add it to the email
    attachment_filename = os.path.basename(attachment_path)
    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type, mime_subtype = mime_type.split('/',1)
    with open(attachment_path, 'rb') as ap:
      message.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype, filename=attachment_filename)

def send_email(message):
  """ Sends he message to tje configured SMTP server."""
  mail_server = smtplib.SMTP('localhost')
  mail_server.send_message(message)
  mail_server.quit()

  #--------------health_check.py-----------------------------------
  #!/usr/bin/env python3
