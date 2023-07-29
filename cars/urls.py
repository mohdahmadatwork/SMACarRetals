from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from cars import views
urlpatterns = [
    path('',views.available_cars,name="index"),
    path('addcar/',views.add_car,name="add car"),
    path('addcarimg/<int:id>',views.add_car_images,name="carimages"),
    path('delete/<int:id>',views.delete_car,name="delete car"),
    path('edit/<int:id>',views.edit_car,name="edit car"),
    path('delete_car_image/<int:id>',views.delete_car_image,name="edit car"),
    path('upload_car_image/',views.upload_image,name="upload image of car"),
    path('<str:str>/',views.car_detail,name="index")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)