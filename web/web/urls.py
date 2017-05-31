from django.conf.urls import url, include
from rest_framework import routers

from app.views import Md5HashViewSet


router = routers.SimpleRouter()
router.register(r"", Md5HashViewSet, base_name="hash")

urlpatterns = [
    url(r"^", include(router.urls))

]
