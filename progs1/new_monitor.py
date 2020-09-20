#!/usr/bin/env python3
import smtplib
import requests
import os
from email.message import EmailMessage

x = []
f = open('sites.txt', 'r')
dns = [line.strip() for line in f if line.strip()]
f.close()
for obj in dns:
    try:
        url = "https://" + obj
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("Site is not reachable ", url)
            f = open("output.txt", "a")
            f.write(url + "\n")
            f.close()
    except:
        print("Invalid URL", url)
        f = open("output.txt", "a")
        f.write(url + "\n")
        f.close()
#    except requests.exceptions.InvalidURL as e:
#        print("Invalid Line", url)
if os.stat('output.txt').st_size == 0:
    #    print('All sites are up. Exiting..')
    exit()
else:
    with open('output.txt', 'r') as fp:
        msg = EmailMessage()
        msg.set_content(fp.read())
        msg['Subject'] = 'Alert!! following sites are not responding. Please check'
        msg['From'] = 'donotreply@mercer.com'
        msg['To'] = 'nitesh.kumar2@mercer.com'
        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()

    file = open("output.txt","r+")
    file.truncate(0)
    file.close()
