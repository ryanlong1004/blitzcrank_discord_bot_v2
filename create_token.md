# How to create a bot with an access token for discord

## The point of this guide is to create a test server to use the bot.

1. Create an account for discord (You should already have this)

2. Acesss discord.com/developers

If you are not already in "Applications", select it from the left sidebar.

This will show a list of bots you currently own.

1. On the top right, press "New Application", and give your bot a name. "Test"

2. Now click on "Bot" on the left side menu

Scroll down a bit further below Priviligues Gateway Intents:

Enable the following intents: Presence Intent, Server Members Intent and Message Content Intent

Click on "Reset Token" and get a new token.

**Note this token down, as you will need it to access the bot.**

4. Go to "Installation"

* Note: You must create a discord server or own a discord server. I suggest creating a new one.

Under "Install Link" copy the link and go to it via your browser.

You will be prompted to add the discord bot, add to discord and than add to your server.

5. Create a .env file to access the bot

Example:

```
BOT_NAME="Test"
DISCORD_TOKEN="YourDiscordTokenHere"
```