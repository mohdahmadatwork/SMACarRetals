from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from home import views
urlpatterns = [
    path('',views.home,name="index"),
    path('about/',views.about,name="about"),
    path('contactus/',views.contactusf,name="contact")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)