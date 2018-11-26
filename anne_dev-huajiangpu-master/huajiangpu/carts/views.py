from django.shortcuts import render


def index(request):
    return render(request, 'carts/cart_cart.html', locals())


