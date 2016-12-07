# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import get_object_or_404, render
from .models import Product, Food, Amount, Company
from django.contrib.auth.decorators import login_required

from locale import *
import csv


@login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = { 'latest_question_list': latest_question_list,
    }
    return render(request, 'selosteet/index.html', context)


@login_required
def products(request):
    companies = Company.objects.filter(user=request.user);
    if( request.user.is_superuser ):
        companies = Company.objects.all()

    product_list = Product.objects.filter(company__in=companies).order_by('name')[:500]

    context = { 'product_list': product_list,
    }
    return render(request, 'selosteet/products.html', context)

@login_required
def food(request, food_id):
    f = get_object_or_404(Food, pk=food_id)
    return render(request, 'selosteet/food.html', {'food': f})

@login_required
def tuote(request, product_id):
    f = get_object_or_404(Product, pk=product_id)
    return render(request, 'selosteet/tuote.html', {'product': f})

@login_required
def tuote2(request, product_id, language_code):
    f = get_object_or_404(Product, pk=product_id)
    return render(request, 'selosteet/tuote2.html', {'product': f, 'language' : language_code})

def setlanguage(request, language_code):
    request.session["language_code"] = language_code
    return HttpResponse("<p>hyv kieli</p>");

def import_foods(request):
    # Full path and name to your csv file
    csv_filepathname="/home/lvp/djangoilua/tuotteet/raaka-aineet.csv"
    setlocale(LC_NUMERIC, 'fi_FI.UTF-8') #atof desimals with ,
    dataReader = csv.reader(open(csv_filepathname, encoding='utf-8'), delimiter=',', quotechar='"')

    next(dataReader, None)  # skip the headers
    n = 0
    out = "<h2>Tuodaan raaka-aineita</h2>"

    for row in dataReader:
        li = ""
        de = ""
        if row[12] is not None and len(row[12]) > 0 and row[12].startswith("http"):
            li = row[12]
        elif ( row[12] is not None and len(row[12]) > 0):
            de = row[12]

        new_food, created = Food.objects.get_or_create(
            extra = row[0],
            name = row[1],
            nameSV = row[2],
            energy = atof(row[3]),
            fat = atof(row[5]),
            saturatedFat = atof(row[6]),
            carbohydrate = atof(row[7]),
            sugar = atof(row[8]),
            fiber = atof(row[9]),
            protein = atof(row[10]),
            salt = atof(row[11]),
            link = li,
            description = de,
            descriptionSV = row[13])
        out += "<pre> Tuodaan( " + str(n) + " )\n"
        out += "   "+new_food.name + "  --  " + new_food.nameSV + "</pre>"
        n += 1

    return HttpResponse(out)



def import_products(request):
    # Full path and name to your csv file
    csv_filepathname="/home/lvp/djangoilua/tuotteet/reseptit.csv"
    setlocale(LC_NUMERIC, 'fi_FI.UTF-8')
    dataReader = csv.reader(open(csv_filepathname, encoding='utf-8'), delimiter=',', quotechar='"')


    out = "<h2>Tuodaan reseptit</h2>"

    new_product = False
    n = 0
    for row in dataReader:
        out += "--rivi--" + str(n) + "--"
        n += 1
        # a new product recipe
        if row[0] == "Resepti":
            new_name = row[1]
            if new_name.isspace():
                continue

            out += "<h3>" +  new_name + "</h3>"
            new_product, created = Product.objects.get_or_create(name = new_name)
            new_product.nameSV = row[2]
            new_product.save()
            continue

        # recipe column names elikkas data descriptions
        if row[0].startswith('aines'):
            continue

        if new_product is False:
            continue

        try:
            recipe_food = Food.objects.get(name = row[0])
        except Food.DoesNotExist:
            out += "<pre>Ei tunneta raaka-ainetta, jonka nimi on "
            out += row[0] + "</pre>"
            continue
        except Food.MultipleObjectsReturned:
            out += "<pre>L&ouml;yty useita raaka-aineita nimell&auml;  "
            out += row[0] + "</pre>"
            continue

        out += recipe_food.name + "<br/>"

        new_amount, created = Amount.objects.get_or_create(
            food = recipe_food,
            product = new_product,
            weight = row[1]
        )
        out += "<pre>   Reseptinro: %s uus raaka-aine %s m&auml;&auml;r&auml; %s</pre> " % (new_product.id, recipe_food.id, row[1])

    return HttpResponse(out)
