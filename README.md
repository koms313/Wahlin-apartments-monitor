# Wahlin-apartments-monitor
This is a script that monitor certain webpage for new apartments, and when interesting apartment is seen, it automatically create an application

# Problem
If you are living in Sweden and new to Stockholm, you will understand the problem with finding an apartment. You have to be registered in a queue and then it takes at least 8 years to be able to get a good apartment using the queue. There are some companies that have some shortcuts. They have their own queue where people are selected "randomly" and not based in first in first served. One of these companies is Wahlin (http://wahlinfastigheter.se/lediga-objekt/lagenhet/) where they place apartments in the page during the weekdays between 1:00 and 2:00 (I found that they sometimes post between 11:00 and 15:00). Of those who applied for the shown apartments during that perioud, one will be selected. Because the apartment display and application perioud is in the middle of the working day, it is annoying to open the browser and keep refershing during the same working day. I needed a way to know when aparatments are displayed. At the begining I used Google chrome extension that allowed me to know if the page has changes, and that worked fine. After a while I got tired of manually applying and also sometimes I missed the application perioud when I was in meetings.

I have created the script in this repository to monitor that page for new apartments, and to apply automatically when there is an apratment with rent less than 8000 sek. The script also send an email notification when it successfully apply for an apartment. I ran the script in my always own raspberry pi. The script has all the parameters hardcoded and it is fairly simple. I am sharing it here so if someone want to use it for himself (only for those living in Stockholm/Sweden) or get some example for the libraries used (lxml and BeautifulSoup).

lxml was a good library, but I had to move to BeautifulSoup because of poor support for non ascii characters.

# Usage
to use the script, first fill your information in the script and enable your gmail ssmtp (in case you would like to use gmail for sending)
https://support.google.com/accounts/answer/6010255?hl=en

the script uses python3
