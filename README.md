# FAQ_KAI_Bot
FAQ для КНИТУ-КАИ

# How to run (for debian):
- git clone https://github.com/ayazzali/FAQ_KAI_Bot.git
- change token at config.py ( nano config.py ) or settings.ini if you already have it
- apt-get install python3
- apt-get install python3-pip
- pip3 install python-telegram-bot
- python3 start.py

# Running after restart
- nano nano /etc/rc.local
- and put:

  - # for faqBotKai
  - exec 2> /var/log/0KaiFaqBot_from_rc.local.log # send stderr from rc.local to a log file
  - exec 1>&2 # send stdout to the same log file
  - cd /root/FAQ_KAI_Bot
  - nohup python3 start.py >> /root/FAQ_KAI_Bot/kaiBot.log &


