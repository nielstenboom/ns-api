## NS Delay Notifier

This is a small script to notify you on your phone via a pushbullet notification if your usual train commute trips have delays.

### Setup

Fill in all the legs of your journey in [trips.csv](trips.csv), be sure you type the EXACT name of the station and times it shows on the NS-app or website, it will not work properly otherwise.

Then get a NS-API key and a Pushbullet API key and fill these in the .env.dist file and rename it to .env 

Then install the requirements
```
pip install -r requirements.txt
```

And then the script can be called with

```
python src/app.py
```

You will get a notification if in the next 20 minutes a scheduled leg of your trip has a delay.

For this script to be useful it should be scheduled via a cronjob or other task scheduler to run every x minutes on a machine that is always online.

Example cron rule with simple logging:
```
*/5 * * * Mon,Tue,Thu (date; cd /root/ns-delay-notifier; python3.7 src/app.py;) >> /root/ns-delay-notifier/modifier.log
```


