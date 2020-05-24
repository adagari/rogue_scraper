#!/bin/python

from bs4 import BeautifulSoup
import requests, smtplib, time, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main():
	url = scrape()
	send_mail(url)
	exit()
	
def scrape():
	url = 'https://www.roguefitness.com/the-ohio-bar-black-zinc' #url of item
	print("Checking for: " + url)
	while True:
		try:
			response = requests.get(url)
		except requests.exceptions.ConnectionError:
			print("[ERROR] Server did not respond, sleeping 30 seconds.")
			time.sleep(10)
			continue
				
		if response.status_code == 200:
			soup = BeautifulSoup(response.text,"html.parser")
			s = soup.find_all('div',{'class': 'product-options-bottom product-options-bottom-8313'}) #find_all for product, replace
			try:
    				s = s[0].find('div',{'class':'bin-stock-availability'}) #checking to see if item is in stock
			except IndexError:
    				print("[ERROR] Webpage was not correctly parsed.")
    				continue
		else:		
			print("[WARN] Unexpected response code.")
			continue
		
		if s: #if line 28 returned a value, item is not in stock
			print("[INFO] Item is not in stock. Sleeping 60 seconds.")
			time.sleep(60)
			continue

		break
		
	print("[INFO] Item Available: " + url)
	return url
		
def send_mail(url):
    sender_address = 'hackermane1337@gmail.com' #replace with sender email
    sender_pass = ''                            #password for sender
    receiver_address = ''                       #where email is sent
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'This item may be in stock!'
    mail_content = 'Hello,\nThis item appears to be in stock.\n\n' + url + '\n\nSigned,\nHackermane1337' #message format, can be changed
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    print("[INFO] Email sent, " + receiver_address)
    session.quit()

if __name__ == "__main__":
    os.system('clear')
    main()
