from django.shortcuts import render


def carts(request):
    return render(request,'df_carts/cart.html')
