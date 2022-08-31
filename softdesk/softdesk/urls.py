from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from issues import views

# Ici nous créons notre routeur
router = routers.SimpleRouter()
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category/’
router.register('projects', views.ProjectViewset, basename='projects')
router.register('admin/projects', views.AdminProjectViewset, basename='admin-products')
router.register('projects/<int:project_id>/issues', views.ProjectViewset, basename='issues')
router.register('admin/issues', views.AdminProjectViewset, basename='admin-issues')
router.register('projects/<int:project_id>/issues/<int:issue_id>/comments', views.ProjectViewset, basename='comments')
router.register('admin/comments', views.AdminProjectViewset, basename='admin-comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # Il faut bien penser à ajouter les urls du router dans la liste des urls disponibles.
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
