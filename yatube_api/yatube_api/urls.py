from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from api import views


router = DefaultRouter()
router.register('api/v1/posts', views.PostViewSet)
router.register('api/v1/groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/posts/<int:pk>/comments/', views.api_comments),
    path('api/v1/posts/<int:pk>/comments/<int:id>/',
         views.api_comments_detail),
    path('api/v1/api-token-auth/', obtain_auth_token),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
