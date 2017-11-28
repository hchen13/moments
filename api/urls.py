from django.conf.urls import url
from rest_framework.routers import DefaultRouter

import api.v1 as v1

app_name = 'api_v1'

router = DefaultRouter()
router.register('user', v1.UserViewSet, base_name='monster')
router.register('moment', v1.MomentViewSet, base_name='moment')

urlpatterns = [
    url(r'^test/$', v1.test),
    url(r'^test/login/$', v1.test_with_login),
]

urlpatterns += router.urls