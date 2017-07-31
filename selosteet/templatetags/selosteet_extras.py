from django import template
from django.template.defaultfilters import stringfilter
from selosteet.models import Allergen
import re
register = template.Library()


@register.filter(name='make_bold')
@stringfilter
def make_bold(str):
    """make bold if in list of allergens"""


    for a in Allergen.objects.all():
        str = re.sub(r"(?P<food>"+a.name+")",r"<b>\1</b>", str)
        if( len(a.nameSV) > 1 ):
            str = re.sub(r"(?P<food>"+a.nameSV+")",r"<p>\1</p>", str)

    return str

"""
    words = str.split()

        for i, w in enumerate(words):
            if( w == a.name ):
                words[i] = '<b>'+ words[i] + '</b>'
            if( w == a.name+"," ):
                words[i] = '<b>'+ words[i] + '</b>'
    #return " ".join(words)

"""
