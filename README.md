# FAQ_KAI_Bot
FAQ для КНИТУ-КАИ
username tg: @FAQ_KAIBot

# How to run (for debian):
- git clone https://github.com/ayazzali/FAQ_KAI_Bot.git
- change token at config.py ( nano config.py ) or settings.ini if you already have it
- apt-get install python3
- apt-get install python3-pip
- pip3 install python-telegram-bot
- python3 start.py

# Running after restart
 - nano /etc/supervisor/supervisord.conf
 - and type at the end this:
 ```
[program:kai_worker]
directory=/root/FAQ_KAI_Bot
command=python3 start.py
;command=nohup python3 start.py >>/root/FAQ_KAI_Bot/log.txt 2>&1
stdout_logfile=/var/log/kai_worker.log
stderr_logfile =/var/log/kai_worker.log
autostart=true
autorestart=true
user=root
stopsignal=KILL
numprocs=1
```
- to check status use command supervisorctl


# Running after restart (method 2)
- nano nano /etc/rc.local
- and put:

  - # for faqBotKai
  - exec 2> /var/log/0KaiFaqBot_from_rc.local.log # send stderr from rc.local to a log file
  - exec 1>&2 # send stdout to the same log file
  - cd /root/FAQ_KAI_Bot
  - nohup python3 start.py >> /root/FAQ_KAI_Bot/kaiBot.log &


