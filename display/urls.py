
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from . import userviews

urlpatterns = [
    path("", views.index_page, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("dashboard/<int:item>", views.dashboard, name="dashboard"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("service/", views.service, name="service"),
    path("logout/", views.logouts, name='logout'),
    path("token/", views.token, name='token'),
    path('verify/<auth_token>', views.verify, name="verify"),
    path('error/', views.error_page, name="error"),
    path("forget_pass/", views.forget_pass, name="forget_pass"),
    path("change_pass/<token>/", views.change_pass, name="change_pass"),
    path("reseterror/", views.reseterror, name="reseterror"),
    path("addtowishlist/",
         userviews.addtowishlist, name="addtowishlist"),
    path("showwishlist/", userviews.showwishlist, name="showwishlist"),
    path('removewishlist/',
         userviews.removewishlist, name='removewishlist'),
    path('removewishlistpage/<int:id>',
         userviews.removewishlistpage, name='removewishlistpage'),
    path('profile/', userviews.profile, name='profile'),
    path('save_profile/', userviews.save_profile, name='save_profile'),
    path('postads/', userviews.postads, name="postads"),
    path('details/<int:item>', userviews.details, name="details"),
    path('uploadads/', userviews.uploadads, name="uploadads"),
    path('soldout/<int:item>',
         userviews.soldout, name='soldout'),
    path('getinformation/', userviews.getinformation, name="getinformation"),   
    path("myorders/", userviews.myorders, name='myorders'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)