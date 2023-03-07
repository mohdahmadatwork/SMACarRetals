from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from orders import views
urlpatterns = [
    path('<int:id>',views.make_order,name="index"),
    path('return/',views.return_car,name="return car"),
    path('detail/<int:id>',views.order_detail,name="details"),
    path('re_rent/<int:id>',views.re_rent,name="re_rent"),
    path('cancel/<int:id>',views.cancel_order,name="cancel_order")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)