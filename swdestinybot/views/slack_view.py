import os
import slack
import json
from django.http import HttpResponse
from django.http import JsonResponse
from swdestinybot.models import Card
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import re
from . import cards_view

client = slack.WebClient(settings.SLACK_TOKEN)

@csrf_exempt
def handle_slack_message(request):
    challenge = json.loads(request.body)
    if challenge['type'] == "url_verification":
        return JsonResponse({ "challenge" : challenge['challenge']})
    elif challenge['type'] == "event_callback":
        return send_message(challenge['event'])

def send_message(event):
    if 'username' not in event and event['type'] == 'message' and 'text' in event:
        text = event['text']
        pattern = re.compile("\[\[(.*)\]\]")
        match = pattern.search(text)
        if match:
            card = match.group(1)
            matchedCards = cards_view.get_cards_from_model(card)
            if len(matchedCards) == 1:
                client.chat_postMessage(
                    channel='#swdestiny',
                    text=matchedCards[0]['name'] + '\n' + matchedCards[0]['image_url'] + '\nFull details: https://swdestinydb.com/card/' + matchedCards[0]['code'])
            elif len(matchedCards) > 1:
                client.chat_postMessage(
                    channel='#swdestiny',
                    text='Multiple matches found for ' + card)
            else:
                client.chat_postMessage(
                    channel='#swdestiny',
                    text='No match found for ' + card)
    return HttpResponse("Ok")
