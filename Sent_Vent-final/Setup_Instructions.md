# Setup Instructions

These instructions should work for Debian and Ubuntu. I recommend running it in a machine with more than 2.25GB RAM memory.

sudo apt-get update  
sudo apt install python3-pip (/OR/) sudo apt-get -y install python3-pip  
pip3 install pandas selenium numpy nltk matplotlib chromedriver_binary  
sudo apt install python3-requests  
sudo apt install git-all  
cd /home/[USERNAME]  
git clone https://github.com/Zeralm/Final "Thesis - Linux optimized"  
sudo apt-get install wget REDUNDANT in UBUNTU 20.  
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb  
sudo apt install ./google-chrome-stable_current_amd64.deb  
sudo apt install screen     (REDUNDANT in UBUNTU 20)  
cd '/Thesis - Linux optimized'/Sent_Vent-final  
screen  
python3 seleCrawl.py [month_before_funding] [telegram_chat_id (optional)]  
alt+a   
alt+d  
(To return it’s:) screen -r [sessionname (optional when there's only one screen)]  
(stop with) ctrl+c  


(If need to reset the tweet data entirely:)  
python3  
import sqlite3  
con = sqlite3.connect("data/ThesisDatabase.db")  
cursorObj = con.cursor()  
con.execute("DELETE FROM tweets")  
con.commit()  
con.close()  
quit()  


(To update a Single file to the new github version, namely seleCrawl.py:)  
screen -r  
cd '/home/[USERNAME]/Thesis - Linux optimized/Sent_Vent-final'  
wget -O seleCrawl.py - https://raw.githubusercontent.com/Zeralm/Final/main/Sent_Vent-final/seleCrawl.py  
vim seleCrawl.py  
python3 seleCrawl.py  



(To reset errorLog file as it eventually gets too large:)  
truncate -s 0 data/errorLog.txt  

 

python3 seleCrawl.py [month_before_funding] [telegram_chat_id -optional-]  


(Reminder for me: connect instantly to any instance with gcloud compute ssh [user@instance] --zone [e.g us-east1-b] using gcloud prompt. Need to configure putty)  



(If there are non bypassable errors on companies with many tweets, the problem is likely memory, you can check: ) 

sudo apt-get install htop  
htop  




(If that’s the case, either get a device with more memory (2,25GB is assured to cause problems already) or somehow optimize usage. Selenium uses a lot of ram, and driver.findelements[...] calls take a sizable toll. Most of them are concentrated in the loop adding links to the set linkos. 
You could also do nothing, and wait for it to eventually fix itself. Sometimes that works.)

