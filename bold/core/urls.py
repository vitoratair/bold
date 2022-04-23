from rest_framework.routers import DefaultRouter

### Resources URLS ###
from core.movies.urls import movies_urlpatterns as movies_urls
from omdb_adapter.urls import omdb_adapter_urlpatterns as omdb_adapter_urls


router = DefaultRouter()

urlpatterns = []

### RESOURCES ###
urlpatterns += movies_urls

### ADAPTERS ###
urlpatterns += omdb_adapter_urls



