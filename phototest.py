import os
import smtplib

path = "/Users/ianmacomber/Python Work/slalom-tokyo-drift"

os.listdir(path)

# ['.DS_Store', '.git', '.phototest.py.swp', 'Photos']

# Test adding a Tuesday to the path

path = path + "/Photos"

path = path + "/Tuesday"

os.chdir(path)

# This finds the oldest file
oldest = min(os.listdir(path), key=os.path.getctime)

# Now let's send it somewhere

fromaddr = 'slalomtokyodrift@gmail.com'
toaddrs = 'ian.d.macomber@gmail.com'

msg = 'This is a test email'

username = 'slalomtokyodrift@gmail.com'
password = 'welpdodge'

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()

server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()
