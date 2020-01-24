
from django.core.management.base import BaseCommand, CommandError
import discord
import re
from django.conf import settings
from ...services import card_service

class DiscordClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        pattern = re.compile("\[\[(.*)\]\]")
        match = pattern.search(message.content)
        if match:
            card = match.group(1)
            matchedCards = []
            try:
                matchedCard = card_service.get_card_by_id(int(card))
                if matchedCard != None:
                    matchedCards.append(matchedCard)
            except ValueError:
                matchedCards = card_service.get_cards_by_name(card)
            if len(matchedCards) == 1:
                await message.channel.send(matchedCards[0]['name'] + " (" + matchedCards[0]['set_name']  + "|" + str(matchedCards[0]['set_number']) + ")" + '\n' + matchedCards[0]['image_url'] + '\nView on swdestinydb.com: https://swdestinydb.com/card/' + matchedCards[0]['code'])
            elif len(matchedCards) > 1:
                output = 'Multiple cards found for ' + card
                for card in matchedCards:
                    output += "\n" + card['name'] + " (" + card['set_name']  + "|" + str(card['set_number']) + ")" + " use: [[" + card['code'] + "]]"
                await message.channel.send(output)
            else:
                await message.channel.send('No card found for ' + card)

class Command(BaseCommand):
    help = 'Connects the discord client'

    def handle(self, *args, **options):
        token = settings.DISCORD_TOKEN
        client = DiscordClient()
        client.run(token)