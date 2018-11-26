from django.conf.urls import url
import views


urlpatterns = [
    url(r'^place_order/$',views.place_order),
]