## How to run

### 1. You need `python3`
So... instal `python3` if you haven't. :)

### 2. You need all requires package
So... Run:
```sh
pip3 install -r requirements.txt
```

### 3. You need to configure discord bot token

How to do that is described [here: writebots.com](https://www.writebots.com/discord-bot-token/).
It's the most important page: [Discord Developer Panel](https://discordapp.com/developers/applications/).

The generated token save in `token.txt` file in the root directory (next to `main.py`).

### 4. Run 🙂

For example by:
```sh
python3 main.py`
```

### 5. Invite and tag bot on your server
It's also descripted [here: writebots.com](https://www.writebots.com/discord-bot-token/).

Good luck!

## Bonus for Linux users
One of the way to run bot in the background of OS.
(It's written by Ubuntu 20.04 user.)

1. Clone repo in to `/var` directory.
2. Create `www` user with correct permissions to read and execute existing files and create files in `files` and `config` directories.
3. Create service config file `/etc/systemd/system/discordbot.service`, with that content:

```
[Unit]
Description=Discord BOT service
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=www
WorkingDirectory=/var/Collector_bot
ExecStart=python3 /var/Collector_bot/main.py
SyslogIdentifier=DiscorBOT

[Install]
WantedBy=multi-user.target
```

4. Run commands:
```sh
sudo systemctl enable discordbot.service
sudo systemctl start discordbot.service
sudo systemctl status discordbot.service
```

5. And if you want to stop bot:
```sh
sudo systemctl stop discordbot.service
```
