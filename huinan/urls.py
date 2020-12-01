from django.conf.urls import url, include
from huinan import views
from rest_framework.routers import DefaultRouter

# 创建路由器并注册我们的视图。
router = DefaultRouter()

# API URL现在由路由器自动确定。
# 另外，我们还要包含可浏览的API的登录URL。
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^echo', views.echo),
    url(r'^heartbeat', views.heartbeat),
    url(r'^checkCode', views.checkCode),
]
