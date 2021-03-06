import debug_toolbar
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from ssm.users.views import UserViewSet, ChangePasswordView, SSMTokenObtainPairView
from ssm.absences.views import AbsenceViewSet
from ssm.assessments.views import AssessmentViewSet, CheckpointViewSet, TaskViewSet
from ssm.skills.views import SkillViewSet
from ssm.projects.views import ProjectViewSet
from ssm.events.views import EventViewSet


admin.autodiscover()
suffix = '' if settings.ENV == 'prd' else f' {settings.ENV.upper()}'
admin.site.site_header = settings.NAME + suffix
admin.site.site_title = settings.NAME + suffix

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'absences', AbsenceViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'assessments', AssessmentViewSet)
router.register(r'checkpoints', CheckpointViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'events', EventViewSet)

urlpatterns = [
    # built-in
    path('admin/', admin.site.urls),

    # 3rd party apps
    path('health/', include('health_check.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

    path('api/v1/token/obtain/', SSMTokenObtainPairView.as_view(), name='auth'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='verify'),

    # our apps
    path('api/v1/', include(router.urls)),
    path('api/v1/change/password/', ChangePasswordView.as_view(), name='change_password'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
