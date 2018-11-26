from django.shortcuts import render


def place_order(request):
    return render(request,'df_order/place_order.html')