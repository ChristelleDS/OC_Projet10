from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from issues import views


router = routers.SimpleRouter()
router.register('projects', views.ProjectViewset, basename='projects')
router.register('admin/projects', views.AdminProjectViewset, basename='admin-products')
router.register('issues', views.IssueViewset, basename='issues')
router.register('admin/issues', views.AdminIssueViewset, basename='admin-issues')
router.register('comments', views.CommentViewset, basename='comments')
# router.register('projects/<int:project_id>/issues/<int:issue_id>/comments', views.CommentViewset, basename='comments')
router.register('admin/comments', views.AdminCommentViewset, basename='admin-comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
