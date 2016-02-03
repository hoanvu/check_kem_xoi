"""Check for new Kem Xoi video."""

# encoding: utf-8
import smtplib
import requests
import pandas as pd

from bs4 import BeautifulSoup
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def send_email(video):
    """Send email to me if new Kem Xoi video was released."""
    sender = 'your_sender_email'
    sender_pass = 'your_sender_email_pass'
    receiver = 'your_receiver_email'

    email_body = "<h1>Kem Xoi <a href='{}'>video {}</a> was released.</h1><br />"\
        .format(video.link[0], video.number[0])

    try:
        body = MIMEText(email_body, 'html')
        email = MIMEMultipart()
        email.attach(body)

        email["Subject"] = "New Kem Xoi Video"
        email["From"] = sender
        email["To"] = receiver

        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()
        server_ssl.login(sender, sender_pass)

        server_ssl.sendmail(sender, receiver, body.as_string())
        server_ssl.close()
    except:
        print "Unable to send email."


def get_video_number(title):
    """Function to get video number from its title."""
    try:
        number = title.split(' ')[3]
        return int(number)
    # If the title's too short, or not a Kem Xoi video, return 0
    except IndexError:
        return 0


def get_new_video_info():
    """Get link, title and number of the latest released video."""
    # Youtube URL for Kem Xoi channel
    url = 'https://www.youtube.com/channel/UCPu7cX9LrVOlCDK905T9tVw'

    # Load URL and parse its contents into BeautifulSoup
    req = requests.get(url, verify=False)
    soup = BeautifulSoup(req.content, 'html.parser')

    # Get titles and URL of all videos in the channel
    # then put them in a Pandas DataFrame
    videos = soup.find_all('a', 'yt-uix-tile-link')
    titles = [video.get('title') for video in videos]
    links = ['https://youtube.com' + video.get('href') for video in videos]

    data = pd.DataFrame({'title': titles, 'link': links})

    # Create a new column that stores video number
    data['number'] = [get_video_number(title) for title in data.title]

    return data.loc[data.number == data.number.max()]


if __name__ == '__main__':
    video = get_new_video_info()

    # Get latest video number stored in max.txt
    video_number_file = 'max.txt'
    with open(video_number_file, 'rb') as f:
        latest_video = f.read()

    latest_video = int(latest_video)

    # If a new Kem Xoi video has been released, write it to max.txt
    # and email user
    if video.number[0] > latest_video:
        with open(video_number_file, 'wb') as f:
            f.write(str(video.number[0]))

        send_email(video)
