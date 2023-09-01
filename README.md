# Nym Monitoring Bot for Telegram

This bot allows to get information about any mixnode on the Nym Mixnet.

When entering the Mix ID of a node, it shows the Identity Key as well as owner's wallet & all the uptime info possible.
In future updates, more detailed info (IP addresses, ports allocated etc.) will be present.

## Installation
1. Make sure you have **python3** installed.
2. Install additional dependencies via **pip install**:
    - *requests*
    - *python-telegram-bot==13.12*
3. Enter your Telegram Bot token retrieved from BotFather (https://t.me/BotFather) in `main.py` on line **229**
4. Launch the bot: `python3 main.py`
