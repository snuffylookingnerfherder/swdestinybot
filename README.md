# swdestinybot
Star Wars Destiny Slack/Discord Bot for referencing card images

# Preview

## Slack

### Single Card Match
![single card match](slack-single.png)

### Multiple Card Match
![multiple card match](slack-multi.png)


## Discord

### Single Card Match
![single card match](discord-single.png)

### Multiple Card Match
![multiple card match](discord-multi.png)


# Running locally
To set up run the following commands using python 3.8
```
python manage.py makemigrations swdestinybot
```

```
python manage.py migrate
```

This sets up the in memory database and schema.

Configure the Slack API Oauth bot tokens by TEAM_ID:TOKEN,TEAM_ID:TOKEN... for your workspace as an environment variable:
```
export SWDESTINY_SLACK_TOKENS='TG713JE7:xoxb-1971234231421342134-9595923459423492-Znp755KasdfasdfaR7TyispkU8'
```

Configure the secret (use your own):
```
export SWDESTINY_SECRET=asdfasdf
```

Configure Debug Mode:
```
export SWDESTINY_DEBUG=True
```

Next to start the service run:
```
python manage.py runserver 0:8000
```

Test hitting the following URLs:
http://localhost:8000/cards

# Discord
For discord, set variable:
```
export DISCORD_TOKEN=asdf
```

To run locally:
```
python manage.py discord_client
```

