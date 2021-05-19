from rareapi.views.post import PostView
from django import urls
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rareapi.views import (Comments, Reactions, TagViewSet, 
                            PostView,register_user, login_user)
                            

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostView, 'post')
router.register(r'comments', Comments, 'comment')
router.register(r'reactions', Reactions, 'reaction')
router.register(r'tags', TagViewSet, 'tag')


urlpatterns = [
    path('', include(router.urls)),
    #path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
