"""swdestinybot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from swdestinybot.views import cards_view
from swdestinybot.views import slack_view
from django.conf import settings

urlpatterns = [
    path('cards', cards_view.handle_request),
    path('slack/events', slack_view.handle_slack_message),
    path('slack/message_actions', slack_view.handle_message_action),
]