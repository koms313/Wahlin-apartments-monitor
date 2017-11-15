# -*- coding: utf-8 -*-
import lxml,time,urllib,smtplib,string,re,sys,datetime
from lxml.html import parse,submit_form
from lxml import etree
from urllib.request import *
from urllib.parse import *
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup

initial_url = 'http://wahlinfastigheter.se/lediga-objekt/lagenhet/'
emailPassword='YourGmailPassword'

def return_interesting_items():
    page = parse(initial_url)
    results = page.xpath("//div[@class='block orange lightgrey-bg fastighet']")
    return results


def apply_for_that_apartment(url):
    page = parse(url).getroot()

    page.forms[0].fields['Förnamn'] = "<FirstName>"

    post_params = {
            "Förnamn" : "<FirstName>",
            "Efternamn" : "<LastName>",
            "Gatuadress" : "CurrentAddress",
            "Postort" : "<City>",
            "Postkod" : "<Zip code>",
            "Typ_av_boende" : "<Current accomodation>",
            "Personnummer" : "<>",
            "E-post" : "<Email>",
            "Telefon" : "<PhoneNumber>",
            "Mobil" : "<MobileNumber>",
            "Arbetsgivare" : "<Company>",
            "Årsinkomst" : "<Yearly Salary>",
            "Hushållet_personer" : "<Number of people in your family>",
            "Hushållet_barn" : "<Number of kids>",
            "message" : "<Some additional information about yourself>",
            'subject' : page.forms[0].fields["subject"],
            'recipient' : page.forms[0].fields["recipient"],
            'objektsnummer' : page.forms[0].fields["objektsnummer"]
            }
    #url = page.forms[0].attrib['action']
    url = 'http://wahlinfastigheter.se/wp-content/plugins/pigmentmail/'
    
    ## The page has some scripting protection, but impersonating Mozilla browser, you can send applications
    request_headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "http://wahlinfastigheter.se",
        "Connection": "keep-alive"
    }
    params = urlencode(post_params).encode('utf-8')
    request = Request(url, headers=request_headers)
    fp = urlopen(request, params)
    soup = BeautifulSoup(fp)
    return soup

def send_email_notification(application_result):
    fromaddr = "<From email>"
    toaddr = "<To email>"
    msg = MIMEMultipart('alternative')
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Applied for an apartment in Wahlin page "+ current_apt_info
    
    body = "We found things that might be interesting to you  " + current_apt_info
    msg.attach(MIMEText(body, 'plain'))

    msg.attach(MIMEText(application_result,'html',_charset='utf-8'))

    # Login to the server and send the message
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo_or_helo_if_needed()
    server.login("<Your login credentials>", emailPassword)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def is_item_worthy(url):
    page = parse(url)
    results = page.xpath("//div[@class='col-xs-12 col-sm-7']")
    values = results[0][1][0][0]
    before=False
    before_key=''
    results_dic={}
    for a in values:
        if len(a) == 1:
            #results_dic.append([a[0].text,''])
            before_key = a[0].text.strip()
            before = True
        elif before:
            results_dic[before_key] = a.text.strip()
            before = False

    s_hyra = results_dic['Hyra']
    s_hyra = re.sub("kr.*", "", s_hyra)
    s_hyra = re.sub("[^0-9]", "", s_hyra)
    hyra = int(s_hyra)

    global current_apt_info
    current_apt_info = ''.join('{}: {}  ,'.format(key, val) for key, val in results_dic.items())
    print (current_apt_info)
    ### I considered apartments with rent of less than 8000 sek
    if hyra < 8000:
        return True
    else:
        return False


def is_item_inside(item, xml_list):
    for each_one in xml_list:
        #print (item[0][0].attrib['title'] + "   " + each_one[0][0].attrib['title'])
        if item[0][0].attrib['title'] == each_one[0][0].attrib['title']:
            return True
    return False


previous_results =  {}
while True:
    try:
        results = return_interesting_items()
        if results:
        # Debug part
            print("found something interesting, list is not empty")
            for item in results:
                if not is_item_inside(item, previous_results):
                    if is_item_worthy(item[0][0].attrib['href']):
                        application_result = apply_for_that_apartment(item[0][0].attrib['href'])
                        send_email_notification(application_result)
        previous_results = results
        current_hour = datetime.datetime.now().time().hour
        if current_hour > 14 or current_hour < 12:
            time.sleep(3600)
        else:
            time.sleep(5)

    except Exception as ex:
        #e = sys.exc_info()[0]
        print( "<p>Error: %s</p>" % ex )
        time.sleep(10)
