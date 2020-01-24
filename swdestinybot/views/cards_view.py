from django.http import HttpResponse
from django.http import JsonResponse
from swdestinybot.models import Card
from django.views.decorators.csrf import csrf_exempt
import requests
from django.forms.models import model_to_dict
from ..services import card_service

@csrf_exempt
def handle_request(request):
    if request.method == "POST":
        return sync_cards()
    else:
        return get_cards(request)

def sync_cards():
    print('Refreshing card cache')
    resp = requests.get('https://swdestinydb.com/api/public/cards')
    if resp.status_code != 200:
        # This means something went wrong.
        return HttpResponse('An error occurred downloading the cards')
    cards = Card.objects.all()
    cards.delete()
    for card in resp.json():
        card_service.save_card(card['code'], card['code'], card['name'], card['name'], card['imagesrc'], card['set_code'], card['position'])
    return HttpResponse('swdestinydb has been synced.')

def get_cards(request):
    name = request.GET.get('name', None)
    return JsonResponse({ "cards" : get_cards_from_model(name)}, safe=False)

def get_cards_from_model(name):
    if name != None:
        return card_service.get_cards_by_name(name)
    else:
        return card_service.get_all_cards()