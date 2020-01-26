"""
Created by sudo-ranjith at 07/01/20

Scenario: this file contains urls and routes
"""

from django.conf.urls import url
from django.urls import path

from .views import home, recommended

urlpatterns = [
    url(r'/home', home, name='home'),
    url(r'/recommended', recommended, name='recommended')

]
