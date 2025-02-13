from django.urls import path, re_path

from export import views


urlpatterns = [
    # API V1 Routes
    path('v1/project/published/', views.PublishedProjectList.as_view(), name='Published_project_list'),
    path('v1/project/published/<str:project_slug>/', views.ProjectVersionList.as_view(),
         name='Published_Project_versions'),
    path('v1/project/published/<str:project_slug>/<str:version>/', views.PublishedProjectDetail.as_view(),
         name='Published_project_detail'),
]

# Parameters for testing URLs (see physionet/test_urls.py)
TEST_DEFAULTS = {
    'project_slug': 'demoeicu',
    'version': '2.0.0',
}
