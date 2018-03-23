"""djangomom_template_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

import os

import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ticket/', include('ticket.urls', namespace='ticket')),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'template_name': 'logout.html'}, name='logout'),
    url(r'^$', views.login_user, name='login_user'),
    url(r'^user_redirection/', views.user_redirection),
    url(r'^change_password/', views.change_password, name='change_password'),
]



# for item in os.listdir(settings.GENERATED_APPS_DIR):
#     if os.path.isfile(os.path.join(settings.GENERATED_APPS_DIR, item, '__init__.py')):
#         app_name = '%s' % item
#         u = url(
#             r'^{0}/'.format(app_name),
#             include(
#                 '{0}.urls'.format(app_name),
#                 namespace='{0}'.format(app_name)
#             )
#         )
#         if u not in urlpatterns:
#             urlpatterns.append(u)