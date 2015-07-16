import os
import smtplib
import datetime as datetime
from time import strftime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

'''
The purpose of this script is to automate emailing out photos to blog,
Photos belong either to a day of week folder or the miscellaneous folder,
This program will check the day of week, navigate to the appropriate folder,
and send out an alternating photo between the day of week and miscellaneous.
The photos should alternate being sent to various members of STD, and sent
to an archive folder once they are emailed out.
'''

# This is the function that sends an email.
# Eventually turn this into a function that accepts arguments
def send_email(filename):
    message = MIMEMultipart()

    # This is the message part of it
    p1 = '<p>Image below hopefully...'
    p2 = '<p>{0}'.format(filename)

    message.attach(MIMEText((p1+p2), 'html'))

    with open(filename, 'rb') as image_file:
        message.attach(MIMEImage(image_file.read()))
    
    fromaddr = 'slalomtokyodrift@gmail.com'
    toaddrs = 'ian.d.macomber@gmail.com'
    
    message['From'] = fromaddr
    message['To'] = toaddrs
    message['Subject'] = 'Python Test E-mail'
    msg_full = message.as_string()
    
    username = 'slalomtokyodrift@gmail.com'
    password = 'welpdodge' # Hide this at somepoint?
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    
    server.login(username,password)
    server.sendmail('slalomtokyodrift@gmail.com', 'ian.d.macomber@gmail.com', msg_full)
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
    send_email(oldest)
    
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
    path = "/Users/ianmacomber/Python Work/slalom-tokyo-drift"
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
