from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from todo.custom_token import CustomObtainAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include('todo.urls')),
    # path('login/', views.obtain_auth_token),
    path('login/', CustomObtainAuthToken.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
