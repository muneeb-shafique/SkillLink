from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # The default admin site
    path('admin/', admin.site.urls),
    
    # INCLUDE all API routes from your core app here:
    path('api/', include('core.urls')),
    
    # Optional: DRF login/logout patterns (useful for testing)
    path('api-auth/', include('rest_framework.urls')),
]