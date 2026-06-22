from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category, Product, Wallet, CartItem, Post, ContactMessage


def get_wallet():

    wallet, created = Wallet.objects.get_or_create(id=1, defaults={'balance': 5000.00})
    return wallet

def get_session_key(request):

    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def home_view(request):

    wallet = get_wallet()
    categories = Category.objects.all()
    trending_products = Product.objects.filter(is_trending=True)
    posts = Post.objects.all().order_by('-id')[:3]
    
    context = {
        'wallet': wallet,
        'categories': categories,
        'trending_products': trending_products,
        'posts': posts
    }
    return render(request, 'index.html', context)

def about_view(request):

    wallet = get_wallet()
    return render(request, 'about.html', {'wallet': wallet})

def shop_view(request):

    wallet = get_wallet()
    products = Product.objects.all()
    categories = Category.objects.all()
    
    context = {
        'wallet': wallet,
        'products': products,
        'categories': categories
    }
    return render(request, 'shop.html', context)

def single_product_view(request, id):

    wallet = get_wallet()
    product = get_object_or_404(Product, id=id)
    return render(request, 'single-product.html', {'wallet': wallet, 'product': product})

def cart_view(request):

    wallet = get_wallet()
    session_key = get_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'wallet': wallet,
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

def add_to_cart_view(request, id):

    product = get_object_or_404(Product, id=id)
    session_key = get_session_key(request)
    
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        session_key=session_key,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    messages.success(request, f"'{product.name}' savatga qoshildi")
    return redirect('home')

def remove_from_cart_view(request, id):
   
    session_key = get_session_key(request)
    cart_item = get_object_or_404(CartItem, id=id, session_key=session_key)
    cart_item.delete()
    messages.success(request, "mahsulot savatdanga tushdi ")
    return redirect('cart')

def checkout_view(request):

    wallet = get_wallet()
    session_key = get_session_key(request)
    cart_items = CartItem.objects.filter(session_key=session_key)
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        if wallet.balance >= total_price and total_price > 0:
            wallet.balance -= total_price
            wallet.save()
            cart_items.delete() 
            messages.success(request, "dastavka")
            return redirect('home')
        else:
            messages.error(request, "pul qomadimi?")

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'wallet': wallet
    }
    return render(request, 'checkout.html', context)
def add_blog_view(request):

    wallet = get_wallet()
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        if title and content:
            Post.objects.create(title=title, content=content, image=image)
            messages.success(request, "yangilik ")
            return redirect('home')
            
    return render(request, 'add_blog.html', {'wallet': wallet})

def add_product_view(request):

    wallet = get_wallet()
    categories = Category.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        is_trending = request.POST.get('is_trending') == 'on'
        
        category = Category.objects.get(id=category_id)
        Product.objects.create(
            name=name, price=price, category=category,
            image=image, is_trending=is_trending
        )
        messages.success(request, f"'{name}' dokonga tushdi ")
        return redirect('home')
        
    return render(request, 'add_product.html', {'wallet': wallet, 'categories': categories})
def blog_list_view(request):
    """Barcha bloglar ro'yxati sahifasi"""
    wallet = get_wallet()
    blogs = Post.objects.all().order_by('-id')
    return render(request, 'blog.html', {'wallet': wallet, 'blogs': blogs})

def blog_detail_view(request, pk):
    wallet = get_wallet()
    blog = get_object_or_404(Post, pk=pk)
    return render(request, 'blog-single.html', {'wallet': wallet, 'blog': blog})

def contact_view(request):
    wallet = get_wallet()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
        messages.success(request, "kirib qosak yozamiz")
        return redirect('contact')
        
    return render(request, 'contact.html', {'wallet': wallet})

def profile_view(request):
    wallet = get_wallet()
    return render(request, 'profile.html', {'wallet': wallet})