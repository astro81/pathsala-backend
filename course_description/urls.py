from rest_framework.routers import DefaultRouter

from course_description import views

router = DefaultRouter()
router.register(r'', views.CourseDescriptionViewSet, basename='course_description')
urlpatterns = router.urls
