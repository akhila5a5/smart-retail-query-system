from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Q
from .models import Product, UserModel, Cart, Orders
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function to convert AI response into valid Django ORM query
def ecommerce_query_to_orm(command):
    prompt = f"""
    You are an expert in Django ORM queries. Convert the following natural language request into a Django ORM query based on this schema:
    
    Schema:
    Table: Product
    Model: Product
    Fields: name (CharField), price (DecimalField), category (CharField), brand (CharField), description (TextField)
    
    Request: {command}
    Django ORM Query (only return the query, no extra text):
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    query = response.text.strip()
    query = re.sub(r'`|"|\'\'\'', '', query)  # Clean response
    
    if "Product.objects" not in query:
        raise ValueError("Invalid ORM query generated.")
    
    return query

# Improved search functionality
def search_products(request):
    search_command = request.GET.get("query", "")
    if not search_command:
        return JsonResponse({"error": "No search query provided!"}, status=400)

    try:
        orm_query = ecommerce_query_to_orm(search_command)
        queryset = eval(orm_query, {"Product": Product})
        product_list = list(queryset.values("id", "name", "price", "category", "brand", "description"))
        return JsonResponse({"products": product_list})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Admin inventory alert system
@receiver(pre_save, sender=Product)
def check_stock(sender, instance, **kwargs):
    if instance.stock < 5:
        messages.warning(None, f"Low stock alert: {instance.name} has less than 5 items left!")

# Other essential views (registration, login, home, product management, cart, orders)
def index(request):
    data = Product.objects.all()
    return render(request, 'index.html', {'data': data})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if UserModel.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('register')
            else:
                UserModel.objects.create(username=username, email=email, password=password)
                messages.success(request, 'User created successfully')
                return redirect('login')
        else:
            messages.error(request, 'Password mismatch')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        if UserModel.objects.filter(email=email, password=password).exists():
            request.session['login'] = 'user'
            request.session['email'] = email
            return redirect('home')
        else:
            messages.error(request, 'Invalid Email or Password')
    return render(request, 'login.html')

def home(request):
    login = request.session.get('login')
    data = Product.objects.all()
    return render(request, 'home.html', {'login': login, 'data': data})

def logout(request):
    request.session.flush()
    return redirect('index')

def upload_products(request):
    if request.method == 'POST':
        product = Product(
            name=request.POST['prductname'],
            price=request.POST['price'],
            description=request.POST['description'],
            image=request.FILES['image'],
            category=request.POST['category'],
            brand=request.POST['brand'],
            stock=int(request.POST.get('stock', 0))
        )
        product.save()
        messages.success(request, 'Product Uploaded Successfully')
        return redirect('uploadproducts')
    return render(request, 'uploadproducts.html')

def cart(request):
    email = request.session.get('email')
    user = UserModel.objects.get(email=email)
    cart_items = Cart.objects.filter(user=user)
    return render(request, 'cart.html', {'cart': cart_items})

def view_orders(request):
    orders = Orders.objects.all()
    return render(request, 'vieworders.html', {'orders': orders})
