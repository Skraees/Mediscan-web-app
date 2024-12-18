from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include('medicine_analyzer.urls')),  # Include app URLs with a prefix
]
