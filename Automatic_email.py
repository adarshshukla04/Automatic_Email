import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import speech_recognition as sr
import yagmail
import pyttsx3
import imaplib
import email

recognizer = sr.Recognizer()

#print(sr.list_microphone_names()) #Function to know device index

#Function to convert text to speech
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

#Function to convert speech to text
def SpeechToText(command):
    return (recognizer.recognize_google(command, language = 'en-us'))

#Function to get correct gmail ID
def changed(address):
    l =[]
    l = address.split()
    address = ""
    for i in l:
        address = address + i
    return address.lower()

#Asking for choice
while(1):
    with sr.Microphone(device_index = 1) as source:
        #Function to clear background noises
        recognizer.adjust_for_ambient_noise(source, duration = 1)
        SpeakText("Choose whether you want to compose mail or read new mail")
        ch = recognizer.listen(source)


        SpeakText("Speak up your mail address")
        sender_address = recognizer.listen(source)
        SpeakText("Speak up your password")
        sender_pass = recognizer.listen(source)

        try:
            choice          = SpeechToText(ch)
            sender_mail     = SpeechToText(sender_address)
            sender_mail     = changed(sender_mail)
            sender_password = SpeechToText(sender_pass)

            sender_mail = "" # <----- Enter Sender mail ID
            sender_password = "" # <---- Enter Password

            print("You said: ", choice)
            print("Your mail address: ", sender_mail)
            #print("Sender Password: ", sender_password)

        except Exception as ex:
            print(ex)



        choice = choice.lower()
#<----------------------------------Compose Mail------------------------------------>
        if (choice == "compose mail"):


            #Function to clear background noises
            recognizer.adjust_for_ambient_noise(source, duration = 1)
            SpeakText("Speak up the receivers mail address")
            receiver_address = recognizer.listen(source)
            SpeakText("Speak up the mail Subject")
            record_subject = recognizer.listen(source)
            SpeakText("Speak up the mail content")
            record_content = recognizer.listen(source)

            try:
                receiver_mail = SpeechToText(receiver_address)
                receiver_mail = changed(receiver_mail)
                mail_content  = SpeechToText(record_content)
                mail_subject  = SpeechToText(record_subject)

                receiver_mail = "" # <---- Enter receiver mail ID

                print("Reciever mail: ", receiver_mail)
                print("Mail Subject: ", mail_subject)
                print("Mail content: ", mail_content)

            except Exception as ex:
                print(ex)

            try:
                message = MIMEMultipart()
                message['From']    = sender_mail
                message['To']      = receiver_mail
                message['Subject'] = mail_subject

                #Using SMTP(Simple Mail Transfer Protocol)

                message.attach(MIMEText(mail_content, 'plain'))
                session = smtplib.SMTP('smtp.gmail.com', 587)

                session.starttls()
                session.login(sender_mail, sender_password)
                text = message.as_string()
                session.sendmail(sender_mail, receiver_mail, text)
                session.quit()
                SpeakText("Mail sent")
                print('Mail Sent')

            except Exception as ex:
                print(ex)

#<-----------------------------Read Mail------------------------------>
        elif (choice == 'read mail'):

            #using IMAP (Internet Mail Access Protocol)
            try:
                host     = 'imap.gmail.com'
                username = sender_mail
                password = sender_password

                mail = imaplib.IMAP4_SSL(host)
                mail.login(username, password)
                mail.select('inbox')
                _, search_data = mail.search(None, 'UNSEEN')

                for num in  search_data[0].split():
                    _, data = mail.fetch(num, '(RFC822)')
                    _, b    = data[0]
                    email_message = email.message_from_bytes(b)
                    for header in ['subject', 'to', 'from', 'data']:
                        SpeakText(header)
                        SpeakText(email_message[header])
                        print("{}: {}".format(header, email_message[header]))


                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode = True)
                            SpeakText("Mail Content")
                            SpeakText(body.decode())
                            print(body.decode())

                        elif part.get_content_type() == "text/html":
                            html_body = part.get_payload(decode = True)
                            print(html_body.decode())

            except Exception as ex:
                print(ex)

        SpeakText("Whether you want to continue or exit")
        ch2 = recognizer.listen(source)
        choice2 = SpeechToText(ch2)
        choice2 = choice2.lower()
        print(choice2)
        if (choice2 == 'exit'):
            exit(0)
        elif (choice2 == 'continue'):
            continue
