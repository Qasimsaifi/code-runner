from django.urls import path, include
from rest_framework import routers
from .views import CodeSnippetViewSet

router = routers.DefaultRouter()
router.register('run-python', CodeSnippetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
