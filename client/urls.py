from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from client import views
urlpatterns = [
    path('',views.dashboard,name="profile"),
    path('login/',views.handlelogin,name="login"),
    path('signup/',views.handlesignup,name="signup"),
    path('logout/',views.handlelogout,name="signup"),
    path('previousorder/',views.previousorderuserside,name="previousorder")
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)