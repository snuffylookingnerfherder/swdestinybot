import discord
import re
from .views import cards_view

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
                matchedCard = cards_view.get_card_by_id(int(card))
                if matchedCard != None:
                    matchedCards.append(matchedCard)
            except ValueError:
                matchedCards = cards_view.get_cards_from_model(card)
            if len(matchedCards) == 1:
                await message.channel.send(matchedCards[0]['name'] + '\n' + matchedCards[0]['image_url'] + '\nView on swdestinydb.com: https://swdestinydb.com/card/' + matchedCards[0]['code'])
            elif len(matchedCards) > 1:
                output = 'Multiple cards found for ' + card
                for card in matchedCards:
                    output += "\n" + card['name'] + " (" + card['set_name']  + "|" + str(card['set_number']) + ")" + " use: [[" + card['code'] + "]]"
                await message.channel.send(output)
            else:
                await message.channel.send('No card found for ' + card)