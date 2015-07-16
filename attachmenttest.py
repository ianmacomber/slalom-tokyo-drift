import os
import smtplib
from time import strftime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

path = "/Users/ianmacomber/Python Work/slalom-tokyo-drift"

os.listdir(path)

# ['.DS_Store', '.git', '.phototest.py.swp', 'Photos']

# Test adding a Tuesday to the path

path = path + "/Photos"

path = path + "/Tuesday"

os.chdir(path)

# This finds the oldest file
oldest = min(os.listdir(path), key=os.path.getctime)

# New approach, we are using a MIME email of mixed type
message = MIMEMultipart()

# This is the message part of it
p1 = '<p>Image below hopefully...'
p2 = '<p>{0}'.format(oldest)

message.attach(MIMEText((p1+p2), 'html'))

with open(oldest, 'rb') as image_file:
    message.attach(MIMEImage(image_file.read()))

# The email part of it
fromaddr = 'slalomtokyodrift@gmail.com'
toaddrs = 'ian.d.macomber@gmail.com'

message['From'] = fromaddr
message['To'] = toaddrs
message['Subject'] = 'Python Test E-mail'
msg_full = message.as_string()

username = 'slalomtokyodrift@gmail.com'
password = 'welpdodge'

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()

server.login(username,password)
server.sendmail('slalomtokyodrift@gmail.com', 'ian.d.macomber@gmail.com', msg_full)
server.quit()

# Next steps

# Move the file to an archive folder
# Change the file name to include a timestamp
# Split the file name out based on the jpg
first, last = oldest.split(".")

newpath = "Archive/" + first + "_" + strftime("%Y_%m_%d") + "." + last

os.rename(oldest, newpath)  # Move the file to the new folder

# I also need to have a .gitignore to make sure I don't git commit the files themselves, only the structure.
