from django.shortcuts import render, get_object_or_404, redirect
from .models import Car, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.shortcuts import render
from ollama import Client
from django.conf import settings


@cache_page(60 * 1)
def index (request):
    cars = Car.objects.all().order_by("price")
    return render(request,'app1/index.html', {"cars": cars})


@login_required(login_url="/users/login/")
def blogs(request):
    search_query = request.GET.get('blogsearch', '')

    cars = Car.objects.filter(name__icontains=search_query)
    if 'reset' in request.GET:
        cars = Car.objects.all()

    return render(request, 'app1/blogs.html', {"cars": cars})

@login_required
def comments(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    comments = car.comment.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = car
            comment.user = request.user
            comment.save()
            return redirect('comments', car_id=car.id)
    else:
        form = CommentForm()

    return render(request, 'app1/comments.html', {
        'car': car,
        'comments': comments,
        'form': form
    })
@cache_page(60 * 2)
def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, 'app1/car_detail.html', {'car': car})

@cache_page(60 * 2)
def list_of_cars(request):
    if 'reset' in request.GET:
        selected_cartypes = []
        min_price = ''
        max_price = ''

    else:
        selected_cartypes = request.GET.getlist('cartype')
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')


    what = request.GET.get('what', 'model')
    isAsc = request.GET.get('isAsc', 'True')


    cars = Car.objects.all()
    if selected_cartypes:
        cars = cars.filter(type__in=selected_cartypes)

    if min_price:
        cars = cars.filter(price__gte=min_price)

    if max_price:
        cars = cars.filter(price__lte=max_price)


    sedan , hatchback , electric, station = "","","",""
    if "Sedan" in selected_cartypes:
        sedan = "checked"
    if "Hatchback" in selected_cartypes:
        hatchback= "checked"
    if "Electric" in selected_cartypes:
        electric = "checked"
    if "Station" in selected_cartypes:
        station = "checked"


    if what == 'price':
        if isAsc == 'True':
            cars = cars.order_by("price")
        else:
            cars = cars.order_by("-price")
    elif what == 'name':
        if isAsc == 'True':
            cars = cars.order_by("name")
        else:
            cars = cars.order_by("-name")
    elif what == 'model':
        if isAsc == 'True':
            cars = cars.order_by("model")
        else:
            cars = cars.order_by("-model")
    elif what == 'type':
        if isAsc == 'True':
            cars = cars.order_by("type")
        else:
            cars = cars.order_by("-type")
    return render(request, 'app1/list_of_cars.html', {
        "cars": cars,
        "what": what,
        "isAsc": isAsc,
        "sedan": sedan,
        "hatchback": hatchback,
        "electric":electric,
        "station": station,
        "min_price": min_price,
        "max_price": max_price
    })

@cache_page(60 * 2)
def car_types(request):
    car_type = request.GET.get('car_type', "Hatchback")
    car_types = Car.objects.filter(type=car_type)

    if 'reset' in request.GET:
        min_price = ''
        max_price = ''
    else:
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')

    what = request.GET.get('what', 'model')
    isAsc = request.GET.get('isAsc', 'True')

    if min_price:
        car_types = car_types.filter(price__gte=min_price)

    if max_price:
        car_types = car_types.filter(price__lte=max_price)

    if what == 'price':
        if isAsc == 'True':
            car_types = car_types.order_by("price")
        else:
            car_types = car_types.order_by("-price")
    elif what == 'name':
        if isAsc == 'True':
            car_types = car_types.order_by("name")
        else:
            car_types = car_types.order_by("-name")
    elif what == 'model':
        if isAsc == 'True':
            car_types = car_types.order_by("model")
        else:
            car_types = car_types.order_by("-model")

    return render(request, 'app1/car_type.html', {
        "car_type": car_type,
        "what": what,
        "isAsc": isAsc,
        "cars": car_types,
        "min_price": min_price,
        "max_price": max_price,
    })

@cache_page(60 * 3)
def search(request):
    if 'reset' in request.GET:
        selected_cartypes = []
        min_price = ''
        max_price = ''

    else:
        selected_cartypes = request.GET.getlist('cartype')
        min_price = request.GET.get('min_price', '')
        max_price = request.GET.get('max_price', '')

    search_query = request.GET.get('search', '')
    what = request.GET.get('what', 'model')
    isAsc = request.GET.get('isAsc', 'True')

    cars = Car.objects.filter(name__icontains=search_query)

    if selected_cartypes:
        cars = cars.filter(type__in=selected_cartypes)

    if min_price:
        cars = cars.filter(price__gte=min_price)

    if max_price:
        cars = cars.filter(price__lte=max_price)


    sedan , hatchback , electric , station= "","","", ""
    if "Sedan" in selected_cartypes:
        sedan = "checked"
    if "Hatchback" in selected_cartypes:
        hatchback= "checked"
    if "Electric" in selected_cartypes:
        electric = "checked"
    if "Station" in selected_cartypes:
        station = "checked"


    if what == 'price':
        if isAsc == 'True':
            cars = cars.order_by("price")
        else:
            cars = cars.order_by("-price")
    elif what == 'name':
        if isAsc == 'True':
            cars = cars.order_by("name")
        else:
            cars = cars.order_by("-name")
    elif what == 'model':
        if isAsc == 'True':
            cars = cars.order_by("model")
        else:
            cars = cars.order_by("-model")
    elif what == 'type':
        if isAsc == 'True':
            cars = cars.order_by("type")
        else:
            cars = cars.order_by("-type")
    return render(request, 'app1/search.html', {
        "cars": cars,
        "what": what,
        "isAsc": isAsc,
        "sedan": sedan,
        "hatchback": hatchback,
        "electric": electric,
        "station": station,
        "min_price": min_price,
        "max_price": max_price,
        "search_query": search_query,
    })
# Create your views here.

from django.db.models import Q
def chat_with_ollama(request):
    user_request = request.GET.get('user_request', '')

    if user_request:
        detected_names, price_range = detect_car_type(user_request)

        cars = Car.objects.all()

        # Filter by car names (exact or partial match)
        if detected_names:
            name_filters = Q()
            for name in detected_names:
                name_filters |= Q(name__icontains=name.strip())
            cars = cars.filter(name_filters)

        # Filter by price range
        if price_range:
            lower_bound, upper_bound = price_range
            if lower_bound and upper_bound:
                cars = cars.filter(price__gte=lower_bound, price__lte=upper_bound)
            elif lower_bound:
                cars = cars.filter(price__gte=lower_bound)
            elif upper_bound:
                cars = cars.filter(price__lte=upper_bound)

        # Sorting logic
        what = request.GET.get('what', 'model')
        isAsc = request.GET.get('isAsc', 'True')

        if what == 'price':
            cars = cars.order_by("price" if isAsc == 'True' else "-price")
        elif what == 'name':
            cars = cars.order_by("name" if isAsc == 'True' else "-name")
        elif what == 'model':
            cars = cars.order_by("model" if isAsc == 'True' else "-model")
        elif what == 'type':
            cars = cars.order_by("type" if isAsc == 'True' else "-type")

        return render(request, "result.html", {
            'user_request': user_request,
            'detected_names': detected_names,
            'price_range': price_range,
            'cars': cars,
            "what": what,
            "isAsc": isAsc,
        })

    return render(request, template_name="chat_form.html")

import ast

def detect_car_type(user_request):
    known_cars = list(Car.objects.values_list('name', flat=True))
    known_cars_str = ', '.join(known_cars)

    prompt = f"""
    You are given a sentence describing cars.

    Known car names: {known_cars_str}

    Task:
    - Identify any specific car names mentioned exactly from the known car names list.
    - Identify car names from the known cars list that match the sentence either by explicit mention OR by matching the car's known features implied by the sentence.
      For example, if the sentence mentions "cars that have a 0-100 under 7 seconds" return all cars from the known list known to have acceleration under 7 seconds.
    - Always identify the price range from the sentence as per rules below.
    - You may return multiple matching cars from the known list if applicable.
    - Match as many cars from the known car names list as possible.
    - Do not limit the number of cars returned unless no match is found.
    
    Price range rules:
        - Only extract price if the sentence explicitly refers to price, money, cost, value, or affordability.
        - "less than X" or "under X" → ["", X]
        - "more than X" or "over X" → [X, ""]
        - "between X and Y" → [X, Y]
        - "cheap" → ["", "2000000"]
        - "expensive" → ["2000000", ""]
        - If nothing about price → ["", ""]
        - Do NOT guess or infer price if not mentioned.

    Format your response exactly as 2 lines, do not use numbering for lists(each item must be on its own line):
    <line 1>: comma-separated car names from known list (or leave empty if none)  
    <line 2>: Python list for price range, e.g. ["", ""]

    Sentence: '{user_request}'
    """

    client = Client(host=settings.OLLAMA['LOCATION'])

    try:
        response = client.chat(
            model=settings.OLLAMA['MODEL'],
            messages=[{"role": "user", "content": prompt}]
        )
        content = response['message']['content'].strip().split('\n')

        print("Full Ollama response:", response)
        car_names = content[0].strip().split(',') if content[0].strip() else []
        price_range = ast.literal_eval(content[1].strip()) if len(content) > 1 else ["", ""]

        print(price_range)
        if price_range[1]:
            try:
                if float(price_range[1]) <= 500000:
                    price_range = ["", ""]
            except ValueError:
                # In case price_range[1] is not a number, reset
                price_range = ["", ""]
        else:
            # If price_range[1] is empty string, reset to ["", ""]
            price_range = ["", ""]



    except Exception as e:
        print("Error:", e)
        car_names = []
        price_range = ["", ""]

    return car_names, price_range

