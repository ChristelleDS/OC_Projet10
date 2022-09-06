from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from issues.views import ProjectViewset, ProjectDetailViewset, \
                        IssueViewset, IssueDetailViewset,\
                        ContributorViewset, ContributorDetailViewset, \
                        CommentViewset, CommentDetailViewset


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('api/signup/', ),
    # path('api/login/', ),
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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
