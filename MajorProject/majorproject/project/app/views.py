from django.shortcuts import render, redirect
from django.contrib import messages

from . models import *

# Create your views here.
def index(request):
    data = Product.objects.all()
    return render(request, 'index.html',{'data':data})


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
                user = UserModel.objects.create(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'User created successfully')
                return redirect('login')
        else:
            messages.error(request, 'Password and Confirm Password not Matched')
            return render(request, 'register.html')


    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == 'admin@gmail.com' and password == 'admin':
            request.session['login']='admin'
            request.session['email']=email
            return redirect('home')
        if UserModel.objects.filter(email=email, password=password).exists():
            request.session['login']='user'
            request.session['email']=email
            return redirect('home')
        else:
            messages.error(request, 'Invalid Email or Password')
            return redirect('login')
    return render(request, 'login.html')


def about(request):
    return render(request, 'about.html')

def home(request):
    data = Product.objects.all()
    login = request.session['login']
    return render(request, 'home.html',{'login':login, 'data':data})

def logout(request):
    del request.session['login']
    del request.session['email']
    return redirect('index')


def uploadproducts(request):
    login = request.session['login']
    if request.method == 'POST':
        product_name = request.POST['prductname']
        product_price = request.POST['price']
        product_description = request.POST['description']
        product_image = request.FILES['image']
        product_category = request.POST['category']
        product_brand = request.POST['brand']
        product_color=request.POST['color']

        data = Product.objects.create(
            name=product_name,
            price=product_price,
            description=product_description,
            image=product_image,
            category=product_category,
            brand=product_brand,
            color=product_color

        )
        data.save()
        messages.success(request, 'Product Uploaded Successfully')
        return redirect('uploadproducts')
        
    return render(request, 'uploadproducts.html',{'login':login})


# import google.generativeai as genai
# from django.http import JsonResponse
# from django.shortcuts import render
# from .models import Product
# import os
# from dotenv import load_dotenv
# import re

# # Load environment variables
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# def ecommerce_query_to_orm(command):
#     prompt =  f"""
#     You are an expert in Django ORM queries. Convert the following natural language request into a Django ORM query based on this schema:

#     Schema:
#     Table: Product
#     Model: Product
#     Fields: name (CharField), price (DecimalField), category (CharField), brand (CharField), description (TextField)

#     Request: {command}
#     Django ORM Query (only return the query, no extra text):
#     """

#     model = genai.GenerativeModel("gemini-pro")
#     response = model.generate_content(prompt)

#     # Extract the query response
#     query = response.text.strip()

#     # Clean the response (remove unnecessary characters)
#     query = re.sub(r'`|"|\'\'\'', '', query)  # Remove unwanted quotes

#     # Ensure it's a valid Django ORM query
#     if "Product.objects" not in query:
#         raise ValueError("Invalid ORM query generated.")

#     return query


# import google.generativeai as genai
# from django.http import JsonResponse
# from django.shortcuts import render
# from .models import Product
# import os
# from dotenv import load_dotenv
# import re

# # Load environment variables
# load_dotenv()

# # Verify API key
# api_key = os.getenv("GEMINI_API_KEY")
# if not api_key:
#     raise ValueError("❌ GEMINI_API_KEY is missing. Check your .env file.")

# # Configure Gemini API
# genai.configure(api_key=api_key)

# def ecommerce_query_to_orm(command):
#     prompt = f"""
#     You are an expert in Django ORM queries. Convert the following natural language request into a Django ORM query based on this schema:

#     Schema:
#     Table: Product
#     Model: Product
#     Fields: name (CharField), price (DecimalField), category (CharField), brand (CharField), description (TextField)

#     Request: {command}
#     Django ORM Query (only return the query, no extra text):
#     """

#     model = genai.GenerativeModel("gemini-1.5-pro-latest")  # ✅ Use correct model
#     response = model.generate_content(prompt)

#     if not response or not hasattr(response, "text"):
#         return JsonResponse({"error": "Failed to get a response from Gemini."})

#     query = response.text.strip()

#     # Clean response
#     query = re.sub(r'`|"|\'\'\'', '', query)  # ✅ Remove unwanted characters

#     # Validate ORM query
#     if not query.startswith("Product.objects."):
#         return JsonResponse({"error": "Invalid query generated: " + query})

#     return query

import google.generativeai as genai
from django.http import JsonResponse
from django.shortcuts import render
from .models import Product
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Verify API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY is missing. Check your .env file.")

# Configure Gemini API
genai.configure(api_key=api_key)

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

    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(prompt)

        # ✅ Check if response is valid
        if not response or not hasattr(response, "text") or not isinstance(response.text, str):
            return JsonResponse({"error": "Invalid response from Gemini AI."})

        query = response.text.strip()

        # ✅ Ensure it's a string before passing to eval()
        if not isinstance(query, str):
            return JsonResponse({"error": "Generated query is not a string."})

        # ✅ Clean response
        query = re.sub(r'`|"|\'\'\'', '', query)

        # ✅ Validate ORM query
        if not query.startswith("Product.objects."):
            return JsonResponse({"error": "Invalid query generated: " + query})

        return query

    except Exception as e:
        return JsonResponse({"error": str(e)})


def search_products(request):
    search_command = request.GET.get("query", "")

    if not search_command:
        return JsonResponse({"error": "No search query provided!"}, status=400)

    try:
        orm_query = ecommerce_query_to_orm(search_command)

        # print('----------------------------------',orm_query,"kmevemgefm--------------------------------------")
        print(f"Generated ORM Query: {orm_query}")
        
        queryset = eval(orm_query, {"Product": Product})
        print(queryset,'hello')   
        # Serialize the query results
        product_list = list(queryset.values())
        # print(product_list, "jwjcwncfsfjsnofiwhqjfo")

        return JsonResponse({"products": product_list})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



def products(request):
    login = request.session['login']
    products = Product.objects.all()
    return render(request, 'products.html',{'login':login,'products':products})


def productdetails(request, id):
    login = request.session['login']
    products = Product.objects.filter(id=id)
    return render(request, 'productdetails.html',{'login':login,'products':products})

def addtocart(request, id):
    login = request.session['login']
    email = request.session['email']
    user =  UserModel.objects.get(email=email)
    product = Product.objects.get(id=id)
    cart = Cart.objects.create(
        user=user,
        product=product
        
    )
    cart.save()
    return redirect('cart')


def cart(request):
    login = request.session['login']
    email = request.session['email']
    user =  UserModel.objects.get(email=email)
    cart = Cart.objects.filter(user=user)
    return render(request, 'cart.html',{'login':login,'cart':cart})


def removefromcart(request, id):
    login = request.session['login']
    email = request.session['email']
    user =  UserModel.objects.get(email=email)
    cart = Cart.objects.get(id=id)
    cart.delete()
    messages.success(request, 'Item Removed Successfully!')
    return redirect('cart')

def buyproduct(request, id):
    login = request.session['login']
    if request.method == 'POST':
        qty = request.POST.get('qty')  # Get the quantity from the form
        print(f"Quantity received: {qty}")
        
        if qty:
            qty = int(qty)  # Convert qty to integer
            # Handle the purchase logic here (e.g., add to the cart or complete the order)
            # You can access the product and qty here
            print(f" Quantity: {qty}")
            product = Cart.objects.get(id=id)
            
            total = product.product.price*qty
            
            return render(request, 'order.html',{'id':id, 'login' : login, 'qty':qty, 'total':total, 'price':product.product.price, 'name' : product.product.name })
            
            # Redirect to a success page or the cart page
            # return redirect('cart')  # Or another appropriate URL


def order(request, id):
    login = request.session['login']
    email = request.session['email']
    if request.method == 'POST':
        name = request.POST.get('name')
        cardnumber = request.POST['cardnumber']
        expdate = request.POST['expdate']
        cvv = request.POST['cvv']
        total = request.POST['total']
        qty = request.POST['qty']
        cart = Cart.objects.get(id=id)
        Orders.objects.create(
            user=UserModel.objects.get(email=email),
            product=cart.product,
            cardholdername=name,
            cardnumber=cardnumber,
            expirationdate=expdate,
            cvv=cvv,
            total_price=float(total),
            quantity=qty
        ).save()
        cart.delete()
        messages.success(request, 'Order Placed Successfully!')
        return redirect('cart')


def vieworders(request):
    login = request.session['login']
    email = request.session['email']
    orders = Orders.objects.filter(status='Order Placed')
    return render(request, 'vieworders.html',{'orders':orders, 'login':login})


def myorders(request):
    login = request.session['login']
    email = request.session['email']
    orders = Orders.objects.filter(user=UserModel.objects.get(email=email))
    return render(request, 'myorders.html',{'orders':orders, 'login':login})

def reject(request, id):
    login = request.session['login']
    order = Orders.objects.get(id=id)
    order.status = 'Rejected'
    order.save()
    if login == 'user':
        messages.success(request, 'Order Rejected Successfully!')

        return redirect('myorders')
    else:
        messages.success(request, 'Order Rejected Successfully!')
        return redirect('vieworders')
    

def accept(request, id):
    login = request.session['login']
    order = Orders.objects.get(id=id)
    order.status = 'Order Delivered'
    order.save()
    messages.success(request, 'Order Delivered Successfully!')
    return redirect('vieworders')
    
from django.db.models import Q
def search(request):
    login = request.session['login']
    search_command = request.GET.get("query", "")
    if search_command:
        products = Product.objects.filter(Q(name__icontains=search_command)|
                                          Q(category=search_command) )
        return render(request, 'products.html',{'products':products, 'login':login})
    else:
        return redirect('products')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product

def update(request, id):
    login = request.session.get('login')
    email = request.session.get('email')
    
    # Get the product based on the provided ID
    products = Product.objects.filter(id=id)
    
    if request.method == 'POST':
        product = Product.objects.get(id=id)

        # Get the data from the form
        product_name = request.POST.get('prductname')
        price = request.POST.get('price')
        brand = request.POST.get('brand')
        category = request.POST.get('category')
        description = request.POST.get('description')
        image = request.FILES.get('image')  # Handle file upload
        color=request.POST.get('color')

        # Update product details
        product.name = product_name
        product.price = price
        product.brand = brand
        product.category = category
        product.description = description
        product.color=color
        # Check if a new image is uploaded
        if image:
            product.image = image
        
        # Save the updated product
        product.save()
        
        # Show success message
        messages.success(request, 'Product updated successfully!')
        
        # Redirect to the page where product list is displayed
        return redirect('products')  # Make sure to update with your actual product list URL

    return render(request, 'update.html', {'product': products, 'login': login, 'id': id})


def delete(request, id):
    # Get the product based on the provided ID
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product Deleted Successfully')
    return redirect('products')
