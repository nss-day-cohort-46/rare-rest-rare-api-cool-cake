from django.urls.conf import include
from django.contrib import admin
from django import urls
from django.urls import path
from rest_framework import routers
from rareapi.views import register_user, login_user
from rareapi.views import Comments, Reactions, TagViewSet, ProfileView, PostView, CategoryViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'categories', CategoryViewSet, 'category')
router.register(r'comments', Comments, 'comment')
router.register(r'reactions', Reactions, 'reaction')
router.register(r'tags', TagViewSet, 'tag')
router.register(r'profiles', ProfileView, 'profile')
router.register(r'posts', PostView, 'post')

urlpatterns = [
    path('', include(router.urls)),
    #path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
