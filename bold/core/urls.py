from rest_framework.routers import DefaultRouter

### Resources URLS ###
from core.movies.urls import movies_urlpatterns as movies_urls

### Adapters URLS ###


router = DefaultRouter()

urlpatterns = []

### RESOURCES ###
urlpatterns += movies_urls

### ADAPTERS ###




