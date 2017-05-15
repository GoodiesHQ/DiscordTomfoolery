# DiscordTomfoolery
A collection of various discord-related tools.


## webhook_spammer.py
Sends multiple HTTP post requests to a webhook URL that will be able to send messages to the designated channel. It does have the ability to mention `@everyone`. This implies that it may have high amount of permissions, so some bots that perform guild-specific checks may actually be able to kick/ban members, although this has not been tested.

#### Help
```python
Usage: webhooker.py [-h] --webhook WEBHOOK --name NAME --avatar-url AVATAR_URL
                    --message MESSAGE [--count COUNT]

optional arguments:
  -h, --help            show this help message and exit
  --webhook WEBHOOK, -w WEBHOOK
                        The Webhook URL
  --name NAME, -n NAME  The name you want to appear on the Bot
  --avatar-url AVATAR_URL, -a AVATAR_URL
                        The avatar image file
  --message MESSAGE, -m MESSAGE
                        The content of the message
  --count COUNT, -c COUNT
                        The number of messages to spam.
```
