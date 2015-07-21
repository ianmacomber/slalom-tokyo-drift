import os
import smtplib
import datetime as datetime
import config
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
def send_video_email(filename):

    message = """From: Slalom Tokyo Drift <slalomtokyodrift@gmail.com>
To: Ian Macomber <ian.d.macomber@gmail.com>
MIME-Version: 1.0
Content-type: text/html
Subject: Video Test
Blog the following video {0}
    """.format(filename)
    
    username = 'slalomtokyodrift@gmail.com'
        
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
        
    server.login(username,config.password)
    server.sendmail('slalomtokyodrift@gmail.com', config.ian, message)
    server.quit()

# This function sends the oldest file in a folder, then moves it to the archive.
def send_oldest_video(path):
    # Find the oldest file in the directory
    # Initially, this could find the archive folder as well.
    filelist = os.listdir(path)
    
    # Get rid of directories, leave only files, send off the oldest file.
    filelist = [f for f in filelist if os.path.isfile(f)]
    oldest = min(filelist, key=os.path.getctime)

    # Send it off in an email
    # You should probably try/except this to make sure files aren't moved if they don't send.
    send_video_email(oldest)
    
    # Send the file to an archive folder
    # For video files, we aren't appending anything -- just moving them.
    filename = oldest[:oldest.rfind(".")]
    ext = oldest[oldest.rfind("."):]

    # Here's where we're putting it, and the title
    newpath = "Archive/" + filename + "_" + strftime("%Y_%m_%d") + ext
    
    # Now let's actually move it
    os.rename(oldest, newpath)

if __name__ == "__main__":
    # This is where my files are located
    path = os.getcwd()  # Set path to the default slalomtokyodriftfolder
    path = path + "/Videos"

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
        send_oldest_video(path)
    else:
        # Move to "Other" and try again
        path = "/Users/ianmacomber/Python Work/slalom-tokyo-drift/Videos/Other"
        os.chdir(path) # Why is this necessary?
        filesleft = len([name for name in os.listdir(path) if os.path.isfile(name)])-1
        if filesleft > 0:
            send_oldest_video(path)
        else:
            print("Out of files!")
