from django.http import HttpResponse
from django.http import JsonResponse
from swdestinybot.models import Card
from django.views.decorators.csrf import csrf_exempt
import requests
import string
from django.forms.models import model_to_dict
# import Queue

# messageQueue = Queue.Queue()
MAX_CARDS = 25

@csrf_exempt
def handle_request(request):
    if request.method == "POST":
        return sync_cards()
    else:
        return get_cards(request)

def get_cards_from_model(name):
    if name != None:
        return list(Card.objects.filter(search__icontains=normalize(name)).values())[:MAX_CARDS]
    else:
        return list(Card.objects.all().values())[:MAX_CARDS]

def get_card_by_id(id):
    return model_to_dict(Card.objects.get(pk=id))

def sync_cards():
    print('Refreshing card cache')
    resp = requests.get('https://swdestinydb.com/api/public/cards')
    if resp.status_code != 200:
        # This means something went wrong.
        return HttpResponse('An error occurred downloading the cards')
    cards = Card.objects.all()
    cards.delete()
    for card in resp.json():
        Card.objects.update_or_create(
            id=int(card['code']),
            code=card['code'],
            name=card['name'], 
            search=normalize(card['name']),
            image_url=card['imagesrc'],
            set_name=card['set_code'],
            set_number=card['position']
        )
    return HttpResponse('swdestinydb has been synced.')

def normalize(name):
    return name.translate(str.maketrans('', '', string.punctuation)).lower().strip()

def get_cards(request):
    name = request.GET.get('name', None)
    return JsonResponse({ "cards" : get_cards_from_model(name)}, safe=False)