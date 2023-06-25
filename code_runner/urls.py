from django.urls import path, include
from rest_framework import routers
from .views import CodeSnippetViewSet

router = routers.DefaultRouter()
router.register('code-snippets', CodeSnippetViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
