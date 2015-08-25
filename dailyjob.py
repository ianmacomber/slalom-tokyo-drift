import os
import smtplib
import datetime as datetime
import config
from time import strftime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

'''
The purpose of this script is to automate emailing out photos and videos to blog,
Photos belong either to a day of week folder or the miscellaneous folder, as do videos
This program will check the day of week, navigate to the appropriate folder,
and send out videos and photos to be blogged.
The photos and videos should alternate being sent to various members of STD, and be moved
to an archive folder once they are emailed out.
'''

# Last done: built a send_email_photo that can do a .cc!
# Next steps:
# Make send_oldest_photo take a primary email
# Build the logic for who gets which emails
# Include the video portion

# Ultimately --
# It's a Thursday.  Send out two videos and three photos to the 5 of us.

# This is the function that sends an email with a photo
# Primary is the person who will be getting the email
def send_email_photo(filename, primary):
    message = MIMEMultipart()    

    # This is the message part of it
    p1 = '<p>Image below hopefully...'
    p2 = '<p>{0}'.format(filename)

    message.attach(MIMEText((p1+p2), 'html'))

    with open(filename, 'rb') as image_file:
        message.attach(MIMEImage(image_file.read()))

    fromaddr = 'slalomtokyodrift@gmail.com'
    toaddrs = config.everyone
    
    message['From'] = fromaddr
    message['To'] = primary
    message['CC'] = ','.join(config.everyone)  # turn the list into a string
    message['Subject'] = 'Python Test E-mail'

    msg_full = message.as_string()
    username = 'slalomtokyodrift@gmail.com'
    password = config.password
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    
    server.login(username,password)
    server.sendmail('slalomtokyodrift@gmail.com', toaddrs, msg_full)
    server.quit()

# This function sends the oldest file in a folder, then moves it to the archive.
def send_oldest_photo(path):
    # Find the oldest file in the directory
    # Initially, this could find the archive folder as well.
    filelist = os.listdir(path)
    
    # Get rid of directories, leave only files, send off the oldest file.
    filelist = [f for f in filelist if os.path.isfile(f)]
    oldest = min(filelist, key=os.path.getctime)

    # Send it off in an email
    # You should probably try/except this to make sure files aren't moved if they don't send.
    # Switch config.ian to whichever person receives the email.
    send_email_photo(oldest, config.ian)
    
    # Send the file to an archive folder
    # Split the string based on the last period to get file name.
    filename = oldest[:oldest.rfind(".")]
    ext = oldest[oldest.rfind("."):]

    # Here's where we're putting it, and the title
    newpath = "Archive/" + filename + "_" + strftime("%Y_%m_%d") + ext
    
    # Now let's actually move it
    os.rename(oldest, newpath)

if __name__ == "__main__":
    # This is where my files are located
    path = os.getcwd()  # Set path to the default slalomtokyodriftfolder
    path = path + "/Photos"

    # Check which day of the week it is
    weekdict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday',
            6: 'Sunday'}
    
    # Change to that path's directory
    dayofweek = weekdict[datetime.datetime.today().weekday()] 
    path = path + "/{0}".format(dayofweek)
    # Eventually I have to figure this out.  Do I move around in the file system or move path?
    os.chdir(path)

    # Check how many files are in that folder
    # This could be done better, but we know there is one folder, so -1.
    filesleft = len([name for name in os.listdir(path) if os.path.isfile(name)])-1

    # Looking at this now, I could combine these functions.
    # If there's a file left, send the oldest file, archive the file.
    if filesleft > 0:
        # Find the file, send the email, move it to archive.
        send_oldest_photo(path)
    else:
        # Move to "Other" and try again
        path = "/Users/ianmacomber/Python Work/slalom-tokyo-drift/Photos/Other"
        os.chdir(path) # Why is this necessary?
        filesleft = len([name for name in os.listdir(path) if os.path.isfile(name)])-1
        if filesleft > 0:
            send_oldest_photo(path)
        else:
            print("Out of files!")
