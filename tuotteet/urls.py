"""
tuotteet URL Configuration
"""

from django.contrib import admin
from django.urls import include, path  # <-- CHANGED

urlpatterns = [
    path('admin/', admin.site.urls),
    # If you want selosteet at the root (i.e. "/"), use an empty path string:
    path('', include('selosteet.urls')),
]
