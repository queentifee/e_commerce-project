from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from .models import Product, Cart, CartItem

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        # Retrieve the cart from the session or create an empty one
        cart = request.session.get('cart', {})

        # Update the cart with the selected product and quantity
        cart[product_id] = cart.get(product_id, 0) + quantity

        # Save the updated cart back to the session
        request.session['cart'] = cart

        messages.success(request, f"{quantity} {product.name}{'s' if quantity > 1 else ''} added to the cart.")

        return redirect('product_detail', product_id=product_id)

    return render(request, 'product_detail.html', {'product': product})
    
@login_required
def add_to_cart(request, product_id):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, pk=product_id)

    # Check if the item is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=user_cart, product=product)

    # If the item is already in the cart, increment the quantity
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('product_list')

@login_required
def view_cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)

    return render(request, 'view_cart.html', {'cart_items': cart_items})

@login_required
def shopping_cart(request):
    # Retrieve the cart from the session or create an empty one
    cart = request.session.get('cart', {})

    # Get the products in the cart
    cart_products = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        subtotal = product.price * quantity
        total_price += subtotal
        cart_products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'shopping_cart.html', {'cart_products': cart_products, 'total_price': total_price})