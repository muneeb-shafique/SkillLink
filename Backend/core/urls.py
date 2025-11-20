from rest_framework.routers import DefaultRouter
from .views import SkillViewSet, SkillProfileViewSet, UserSkillViewSet, EndorsementViewSet, PostViewSet

# 1. Initialize the DefaultRouter
router = DefaultRouter()

# 2. Register all your ViewSets with the router
# This automatically generates all the standard RESTful routes (list, detail, etc.)
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'profiles', SkillProfileViewSet, basename='profile')
router.register(r'userskills', UserSkillViewSet, basename='userskill')
router.register(r'endorsements', EndorsementViewSet, basename='endorsement')
router.register(r'posts', PostViewSet, basename='post')

# 3. Assign the router's generated URLs to the mandatory 'urlpatterns' list
urlpatterns = router.urls