# pavlov-bot
Discord bot to inferface with Pavlov VR RCON


# Setup
*This setup guide assumes you are running Ubuntu 18.04 or later. Later versions may already have required python3.8 version. It also assumes you are running the bot on the same server running pavlovserver following setup guide found [here](http://wiki.pavlov-vr.com/index.php?title=Dedicated_server).*

## Prerequisites
- pip3    
- python3.8    
- pipenv

## Installing pip3
`sudo apt install python3-pip`

## Installing python3.8
Get your system up to date and install some prerequisites 
```
sudo apt update
sudo apt upgrade
sudo apt install software-properties-common
```

Install PPA for Python3.8 by adding the deadsnakes PPA to your system’s sources list:

```
sudo add-apt-repository ppa:deadsnakes/ppa
```
When prompted press Enter to continue

Once the repository is enabled, install Python 3.8 with:

```
sudo apt install python3.8
```

Verify that the installation was successful by typing:
```
python3.8 --version
```

## Getting pavlov-bot code from github and creating config files
*Log in as steam user (or whatever user will run bot. This assumes steam user used for pavlovserver as documented [here](http://wiki.pavlov-vr.com/index.php?title=Dedicated_server)) and run following commands*


```
su - steam 

cd ~ && git clone https://github.com/makupi/pavlov-bot
```
Copy file config.json.default file from Examples directory to `/home/steam/pavlov-bot/config.json` with following single line:
```json
{"prefix": ";", "token": "replacemewithdiscordtoken"}
```

Copy servers.json.default file from Examples directory to `/home/steam/pavlov-bot/servers.json` and edit as required for your servers. Admins in servers.json are discordIDs of the admin users ([how to find user-ids](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)) and IP, port are as required to get to the rcon severs and password is the unhashed password setup in RconSettings.txt.

Note that server names are processed case insensitive, so FL_Rush can be called by ;serverinfo fl_rush

## Setup your bot with discord
Follow instructions [here](https://discordpy.readthedocs.io/en/latest/discord.html#).    
Obtain the bot token and install in config.json

## Installing pipenv
As root user run the following command    
`pip3 install pipenv`

## Setup of pipenv for pavlov-bot
login as steam user    
`cd ~/pavlov-bot && pipenv install`

## Test startup of bot
As steam user run the following command    
`cd ~/pavlov-bot && /usr/local/bin/pipenv run python3.8 run.py`

Go to your discord channel that the bot has been invited to and allowed to read and write to and try a few commands to test. Suggest ``;help`` and ``;info`` as good starters, then ``;servers`` to see if your server.json was read correctly. 

## Make bot run as a systemd service
As root create `/etc/systemd/system/pavlov-bot.service` file with following config:

```ini
[Unit]
Description=Pavlov-bot

[Service]
Type=simple
WorkingDirectory=/home/steam/pavlov-bot
ExecStart=/usr/local/bin/pipenv run python3.8 run.py
RestartSec=1
Restart=always
User=steam
Group=steam

[Install]
WantedBy = multi-user.target
```

As root run following commands:
```
systemctl enable pavlov-bot
systemctl start pavlov-bot
```

Test bot... if all is good, then bot will start with server boot and restart if crashes occur. 

Follow the logs with:    
`journalctl -n 20 -f -u pavlov-bot`

## Updating codebase
pavlov-bot is in active developement and new features will need to be checked out of the 'master' branch which we will try and keep stable. 

To update from master as steam user:

``cd /home/steam/pavlov-bot`` (or wherever you have installed)

``git pull``

``pipenv sync``

Then restart your bot to run version with recent changes. If following this guide:

``systemctl restart pavlov-bot``


# Roles and permissions
The bot has 4 permission levels:
* Everyone (can run ;servers, ;serverinfo, ;players, ;playersinfo ;batch)
* Captain (can run Everyone commands plus ;switchmap, ;resetsnd, ;switchteam, ;rotatemap)
* Mod (can run Captain commands plus ;ban, ;unban, ;kick)
* Admin (can do everything)

## Administration of permissions
* Admins are defined in servers.json all other groups are configured using discord roles. 
* Roles need to be setup in discord using the following format {role name}-{server} where Role names are (Mod,Captain,Banned) and server is as returned by ;server command. Eg: Mod-testserver or Captain-rush

# Known issues with Rcon that bot can't fix
* When a SwitchMap Rcon command is issued, the server always returns true no matter what map (or no valid map at all) was requested. No way to know if the request was valid or not or what will happen. Could be nothing, could be datacenter. It is a mystery. 
* When a SwitchMap Rcon command is successful in changing map, subsequent ServerInfo requests return previous map's data for duration of current map until either a RotateMap command is issued or map ends naturally and rotates to next map.
