from swdestinybot.models import Card
from django.forms.models import model_to_dict
import string

MAX_CARDS = 25

def get_cards_by_name(name):
    cards = Card.objects.filter(search__icontains=normalize(name))
    return list(cards.values())[:MAX_CARDS]
  
def get_all_cards():
    cards = Card.objects.all()
    return list(cards.values())

def get_card_by_id(id):
    return model_to_dict(Card.objects.get(pk=id))

def save_card(id, code, name, search, image_url, set_name, set_number):
    return  Card.objects.update_or_create(
        id=int(id),
        code=code,
        name=name,
        search=normalize(search),
        image_url=image_url,
        set_name=set_name,
        set_number=set_number
    )

def normalize(name):
    return name.translate(str.maketrans('', '', string.punctuation)).lower().strip()