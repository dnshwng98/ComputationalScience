"""
URL configuration for ComputationalScienceProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from earthquake import views as earthquake_views
from spotify import views as spotify_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Earthquake URLS
    path('earthquake/check/', earthquake_views.check, name="earthquake-check"),
    path('earthquake/retrieve-data/', earthquake_views.retrieve_data, name="earthquake-retrieve-data"),
    path('earthquake/collect-new-data/', earthquake_views.collect_new_data, name="earthquake-collect-new-data"),
    path('earthquake/check-the-amount-of-new-data-available/', earthquake_views.check_the_amount_of_new_data_available,
         name="earthquake-check-the-amount-of-new-data-available"),

    # Spotify URLS
    path('spotify/retrieve-data/', spotify_views.retrieve_data, name="spotify-retrieve-data"),
    path('spotify/color-gradation/', spotify_views.color_gradation, name="spotify-color-gradation"),
]
