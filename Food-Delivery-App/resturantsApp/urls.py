from django.urls import path
from .views import resturantsList
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('resturants/', resturantsList.as_view(), name='resturantslist'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)