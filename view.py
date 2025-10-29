from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem, Order

# Product listing
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# Product details
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

# Add to cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(product=product)
    item.quantity += 1
    item.save()
    return redirect('cart')

# View cart
def cart_view(request):
    items = CartItem.objects.all()
    total = sum(item.subtotal() for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})

# Order process
def place_order(request):
    items = CartItem.objects.all()
    total = sum(item.subtotal() for item in items)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        Order.objects.create(customer_name=name, customer_email=email, total=total)
        items.delete()  # Clear cart after order
        return render(request, 'order_success.html', {'name': name})
    return render(request, 'cart.html', {'items': items, 'total': total})
