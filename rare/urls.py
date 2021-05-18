from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rareapi.views import register_user, login_user
from rest_framework import routers
from rareapi.views import Comments

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'comments', Comments, 'comment')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),

]
