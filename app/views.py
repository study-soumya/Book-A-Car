from django.shortcuts import(
    render, redirect, HttpResponseRedirect,get_object_or_404
)
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def get_car_dealer(request):
    user = request.user
    if user.is_authenticated:
        return get_object_or_404(CarDealer, car_dealer=user)
    return None

def index(request):
    cars = Car.objects.all()
    context = {
        'cars':cars
    }
    return render(request, 'index.html', context)

def customer_signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, "Password didn't match. Try again!")
            return redirect('customer_signup')
        
        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password1)
        
        user.save()
        
        try:
            location = Location.objects.get(city=city)
        except:
            location = None
        if location is not None:
            customer = Customer(user=user, phone=phone, location=location, type="Customer")
        else:
            location = Location(city=city)
            location.save()
            location = Location.objects.get(city=city)
            customer = Customer(user=user, phone=phone, location=location, type="Customer")
            
        customer.save()
        messages.success(request, 'Your account has been created successfully.')
        return redirect('customer_login')
        
    return render(request, 'customer_signup.html')

def customer_login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                user1 = Customer.objects.get(user=user)
                if user1.type == 'Customer':
                    login(request, user)
                    return redirect('customer_homepage')
            else:
                messages.error(request, 'Invalid credentials or account type.')
    except Exception as e:
        print(e)
        messages.error(request, 'User does not exist! Please enter valid username')
        return redirect('customer_login')
    
    return render(request, 'customer_login.html')

def car_dealer_signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Invalid Credentials')
            return redirect('car_dealer_signup')
        
        if city:
            try:
                location = Location.objects.get(city=city)
            except Location.DoesNotExist:
                
                location = Location(city=city)
                location.save()
        else:
            messages.error(request, 'Please provide a valid city.')
            return redirect('car_dealer_signup')
        
        user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password1)
        user.save()
        

        car_dealer = CarDealer(car_dealer=user, phone=phone, location=location, type='Car Dealer')
        car_dealer.save()
        
        messages.success(request, 'Your account has been created successfully.')
        return redirect('car_dealer_login')
    
    return render(request, 'car_dealer_signup.html')

def car_dealer_login(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = CarDealer.objects.get(car_dealer=user)
                if user1.type == 'Car Dealer':
                    login(request, user)
                    return redirect('all_cars')
                else:
                    messages.error(request, 'Invalid credentials or account type.')
    except Exception as e:
        print(e)
        messages.error(request, 'User does not exist! Please enter valid username')
        return redirect('car_dealer_login')
        
    return render(request, 'car_dealer_login.html')

def signout(request):
    logout(request)
    return redirect('index')

@login_required(login_url='car_dealer_login')
def add_car(request):
    if request.method == 'POST':
        car_name = request.POST.get('car_name')
        city = request.POST.get('city')
        image = request.FILES.get('image')
        capacity = request.POST.get('capacity')
        rent = request.POST.get('rent')
        car_dealer = CarDealer.objects.get(car_dealer=request.user)
        
        try:
            location = Location.objects.get(city=city)
        except:
            location = None
        if location is not None:
            car = Car(name=car_name, car_dealer=car_dealer, location=location, capacity=capacity, image=image, rent=rent)
        else:
            location = Location(city=city)
            location.save()
            car = Car(name=car_name, car_dealer=car_dealer, location=location, capacity=capacity, image=image, rent=rent)
            
        car.save()
        messages.success(request, 'Car added successfully.')
        return redirect('all_cars')
        
    return render(request, 'add_car.html')

@login_required(login_url='car_dealer_login')
def all_cars(request):
    car_dealer = get_car_dealer(request)
    if car_dealer:
        cars = Car.objects.filter(car_dealer=car_dealer)
    else:
        cars = []
    
    return render(request, 'all_cars.html', {'cars':cars})

@login_required(login_url='car_dealer_login')
def edit_car(request, myid):
    car_dealer = get_car_dealer(request)
    car = get_object_or_404(Car, id=myid, car_dealer=car_dealer)
    if request.method == 'POST':
        car_name = request.POST.get('car_name')
        city = request.POST.get('city')
        capacity = request.POST.get('capacity')
        rent = request.POST.get('rent')
        
        car.name = car_name
        car.city = city
        car.capacity = capacity
        car.rent = rent
        image = request.FILES.get('image')
        
        if image:
            car.image = image
        
        car.save()
        
        messages.success(request, 'Car details updated successfully.')
        return redirect('all_cars')
    return render(request, 'edit_car.html', {'car':car})

@login_required(login_url='car_dealer_login')
def delete_car(request, myid):
    car_dealer = get_car_dealer(request)
    car = get_object_or_404(Car, id=myid, car_dealer=car_dealer)
    car.delete()
    return redirect('all_cars')

@login_required(login_url='customer_login')
def customer_homepage(request):
    return render(request, 'customer_homepage.html')

@login_required(login_url='customer_login')
def search_results(request):
    if request.method == 'POST':
        city = request.POST.get('city').title()
        vehicles_list = []
        location = Location.objects.filter(city=city)
        for a in location:
            cars = Car.objects.filter(location=a)
            for car in cars:
                if car.is_available:
                    vehicle_dictionary = {
                        'name': car.name,
                        'id': car.id,
                        'image': car.image.url,
                        'city': car.location.city,
                        'capacity': car.capacity,
                        'rent':car.rent
                    }
                    vehicles_list.append(vehicle_dictionary)
        request.session['vehicles_list'] = vehicles_list
        return render(request, 'search_results.html')

    return redirect('index')

@login_required(login_url='customer_login')
def car_rent(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user = request.user
        car = Car.objects.get(id=id)
        cost_per_day = int(car.rent)
        context = {
            'car': car,
            'cost_per_day': cost_per_day
        }
        return render(request, 'car_rent.html', context)
    messages.success(request, f"Congratulations {user.get_full_name.title()}, {car.name} is booked successfully.")
    
    return redirect('order_details')

@login_required(login_url='customer_login')
def order_details(request):
    if request.method == 'POST':
        car_id = request.POST.get('id')
        username = request.user
        user = User.objects.get(username=username)
        days = request.POST.get('days')
        car = Car.objects.get(id=car_id)

        if car.is_available:
            car_dealer = car.car_dealer
            rent = (int(car.rent)) * (int(days))
            car_dealer.earnings += rent
            car_dealer.save()

            try:
                order = Order(car=car, car_dealer=car_dealer, user=user, rent=rent, days=days)
                order.save()
            except:
                order = Order.objects.get(car=car, car_dealer=car_dealer, user=user, rent=rent, days=days)
            car.is_available = False
            car.save()
            messages.success(request, "Your order is placed successfully. You can now get the car from us.")
            return render(request, 'order_details.html', {'order': order})

    return redirect('past_orders')

@login_required(login_url='customer_login')
def past_orders(request):
    user = request.user
    if user.is_authenticated:
        all_orders = Order.objects.filter(user=user, is_complete=False)
    else:
        all_orders = []
    return render(request, 'past_orders.html', {'all_orders': all_orders})

@login_required(login_url='customer_login')
def delete_order(request, myid):
    order = get_object_or_404(Order, id=myid, user=request.user, is_complete=False)
    order.delete()
    messages.success(request, "Your order deleted successfully.")
    return redirect('past_orders')

@login_required(login_url='car_dealer_login')
def all_orders(request):
    car_dealer = get_car_dealer(request)
    if car_dealer:
        all_orders = Order.objects.filter(car_dealer=car_dealer, is_complete=False)
    else:
        all_orders = []
    return render(request, 'all_orders.html', {'all_orders': all_orders})

@login_required(login_url='car_dealer_login')
def complete_order(request):
    if request.method == 'POST':
        order_id = request.POST['id']
        order = get_object_or_404(Order, id=order_id, car_dealer=get_car_dealer(request), is_complete=False)
        car = order.car
        order.is_complete = True
        order.save()
        car.is_available = True
        car.save()
        messages.success(request, 'Order completed successfully.')
        return redirect('all_orders')

    return redirect('all_orders')

@login_required(login_url='car_dealer_login')
def earnings(request):
    car_dealer = get_car_dealer(request)
    if car_dealer:
        orders = Order.objects.filter(car_dealer=car_dealer)
    else:
        orders = []
    return render(request, 'earnings.html', {'amount': car_dealer.earnings, 'all_orders': orders})