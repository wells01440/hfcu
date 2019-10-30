import smtplib

# Import the email_examples modules we'll need
from email_examples.message import EmailMessage

text_file = "/tmp/blah"

# Open text file whose name is in textfile for reading.
with open(textfile) as fp:
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(fp.read())

# me == the sender's email_examples address
# you == the recipient's email_examples address
msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server.
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()
