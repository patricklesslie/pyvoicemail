# Import smtplib for the actual sending function
import smtplib
import mimetypes

# Here are the email package modules we'll need
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '

# Create the container (outer) email message.
msg = MIMEMultipart()
msg['Subject'] = 'Voicemail'
# me == the sender's email address
# family = the list of all recipients' email addresses
msg['From'] = 'patrick@new.asylumseekerscentre.org.au'
#msg['To'] = COMMASPACE.join(family)
msg['To'] = 'patrick@lesslie.com.au'
#msg.preamble = 'Our family reunion'

path = 'test.mp3'
ctype, encoding = mimetypes.guess_type(path)
maintype, subtype = ctype.split('/', 1)

fp = open(path, 'rb')
voice = MIMEAudio(fp.read(),_subtype=subtype)
fp.close()
voice.add_header('Content-Disposition', 'attachment', filename='voice.mp3')
msg.attach(voice)

# Send the email via our own SMTP server.
s = smtplib.SMTP('localhost')
server.set_debuglevel(1)
s.sendmail(msg['From'], msg['To'], msg.as_string())
s.quit()

#
#import smtplib
#
#def prompt(prompt):
#    return raw_input(prompt).strip()
#
#fromaddr = prompt("From: ")
#toaddrs  = prompt("To: ").split()
#print "Enter message, end with ^D (Unix) or ^Z (Windows):"
#
## Add the From: and To: headers at the start!
#msg = ("From: %s\r\nTo: %s\r\n\r\n"
#       % (fromaddr, ", ".join(toaddrs)))
#while 1:
#    try:
#        line = raw_input()
#    except EOFError:
#        break
#    if not line:
#        break
#    msg = msg + line
#
#print "Message length is " + repr(len(msg))
#
#server = smtplib.SMTP('localhost')
#server.set_debuglevel(1)
#server.sendmail(fromaddr, toaddrs, msg)
#server.quit()
