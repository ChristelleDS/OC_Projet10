from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from issues.views import ProjectViewset, IssueViewset, ContributorViewset, CommentViewset
                         # IssueDetailViewset, ContributorDetailViewset, CommentDetailViewset, UserViewset, ProjectDetailViewset,
from authentication.views import CreateUserAPIView



router = routers.SimpleRouter()
router.register(r'projects', ProjectViewset, basename='projects')
## generates:
# /projects/
# /projects/{pk}/

issue_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
issue_router.register(r'issues', IssueViewset, basename='issues')
## generates:
# /projects/{project_pk}/issues/
# /projects/{project_pk}/issues/{pk}/

user_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
user_router.register(r'users', ContributorViewset, basename='users')
## generates:
# /projects/{project_pk}/users/
# /projects/{project_pk}/users/{pk}/

comment_router = routers.NestedSimpleRouter(issue_router, r'issues', lookup='issue')
comment_router.register(r'comments', CommentViewset, basename='comments')
## generates:
# /projects/{project_pk}/users/{user_pk}/comments/
# /projects/{project_pk}/users/{user_pk}/comments/{pk}/

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/login/', include('rest_framework.urls')),
    path('api/signup/', CreateUserAPIView.as_view(), name='signup'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path(r'api/', include(router.urls)),
    path(r'api/', include(issue_router.urls)),
    path(r'api/', include(user_router.urls)),
    path(r'api/', include(comment_router.urls)),

]

"""
    path('api/projects/', ProjectViewset.as_view(), name='project_cl'),
    path('api/projects/<int:pk>/', ProjectDetailViewset.as_view(), name='project_rud'),
    path('api/projects/<int:project_id>/users/', ContributorViewset.as_view(), name='contrib_cl'),
    path('api/projects/<int:project_id>/users/<int:pk>/',
        ContributorDetailViewset.as_view(), name='contrib_rud'),
    path('api/projects/<int:project_id>/issues/', IssueViewset.as_view(), name='issue_cl'),
    path('api/projects/<int:project_id>/issues/<int:pk>/',
        IssueDetailViewset.as_view(), name='issue_rud'),
    path('api/projects/<int:project_id>/issues/<int:issue_id>/comments/',
        CommentViewset.as_view(), name='comment_cl'),
    path('api/projects/<int:project_id>/issues/<int:issue_id>/comments/<int:pk>/',
        CommentDetailViewset.as_view(), name='comment_rud'),
"""