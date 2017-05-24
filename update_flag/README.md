# TeamFive/update_flag

Flag Update Service for Government.

Written in Python 2.7 and python-gnupg 


## Requirements

- Python 2.7
- python-gnupg 


## GPG keys 

For executing flag updater, we need one team private key and TA's public keys.   
In `takeys` folder, I gather the TA's public keys.   
Public key must be named as `GithubID.pub`   

## Setup

    sudo pip install -r requirements.txt

## Run

    sudo python keyserver.py [TEAM_Private_Key_File] [TA's_Public_Key_Folder]
