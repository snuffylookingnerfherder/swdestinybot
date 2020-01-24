import os
import slack
import json
from django.http import HttpResponse
from django.http import JsonResponse
from swdestinybot.models import Card
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import re
from ..services import card_service
from urllib.parse import unquote

clients = {}

@csrf_exempt
def handle_slack_message(request):
    payload = json.loads(request.body)
    if payload['type'] == "url_verification":
        return JsonResponse({ "challenge" : payload['challenge']})
    elif payload['type'] == "event_callback":
        return send_message(payload['event'])

@csrf_exempt
def handle_message_action(request):
    if request.method == 'POST':
        action = json.loads(request.POST.get('payload'))
        if action['type'] == "block_actions":
            cardId = action['actions'][0]['value']
            matchedCard = card_service.get_card_by_id(int(cardId))
            if matchedCard != None:
                getClient(action['team']['id']).chat_postMessage(
                    channel='#swdestiny',
                    text=matchedCard['name'] + '\n' + matchedCard['image_url'] + '\nFull details: https://swdestinydb.com/card/' + matchedCard['code'],
                    blocks=buildCardResponse(matchedCard),
                    unfurl_links=False)
    return HttpResponse("Ok")

def send_message(event):
    if 'username' not in event and event['type'] == 'message' and 'text' in event:
        text = event['text']
        pattern = re.compile("\[\[(.*)\]\]")
        match = pattern.search(text)
        if match:
            card = match.group(1)
            matchedCards = card_service.get_cards_by_name(card)

            if len(matchedCards) == 1:
                getClient(event['team']).chat_postMessage(
                    channel='#swdestiny',
                    text=matchedCards[0]['name'] + '\n' + matchedCards[0]['image_url'] + '\nFull details: https://swdestinydb.com/card/' + matchedCards[0]['code'],
                    blocks=buildCardResponse(matchedCards[0]),
                    unfurl_links=False)
            elif len(matchedCards) > 1:
                getClient(event['team']).chat_postMessage(
                    channel='#swdestiny',
                    text='Multiple cards found for ' + card,
                    blocks=buildMultipleResponse(card, matchedCards))
            else:
                getClient(event['team']).chat_postMessage(
                    channel='#swdestiny',
                    text='No card found for ' + card)
    return HttpResponse("Ok")

def buildCardResponse(matchedCard):
    return [
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*" + matchedCard['name'] + " (" + matchedCard['set_name'] + "|" + str(matchedCard['set_number']) + ")" + "*"
			}
        },
        {
            "type": "image",
            "block_id": "image1",
            "image_url": matchedCard['image_url'],
            "alt_text": matchedCard['name']
        },
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "<https://swdestinydb.com/card/" + matchedCard['code'] + "| View on swdestinydb.com>"
			}
        }
    ]

def buildMultipleResponse(cardName, matchedCards):
    blocks = [
        {
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Multiple cards found for *" + cardName + "*"
			}
        },
        {"type": "actions"}
    ]
    elements = []
    for card in matchedCards:
        elements.append({
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": card['name'] + " (" + card['set_name']  + "|" + str(card['set_number']) + ")"
            },
            "value": card['code'],
            "action_id": card['code']
        })
    blocks[1]['elements'] = elements
    return blocks

def getClient(teamId):
    if teamId not in clients:
        token = settings.SLACK_TOKENS[teamId]
        clients[teamId] = slack.WebClient(token)

    return clients[teamId]