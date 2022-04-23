from django.urls import path
from omdb_adapter.views import OmdbSyncAPIView

omdb_adapter_urlpatterns = [
    path('omdb/sync/', OmdbSyncAPIView.as_view(), name="omdb_sync"),
]
