from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Skill, SkillProfile, UserSkill, Post, Endorsement
from .serializers import (
    SkillSerializer, SkillProfileSerializer, 
    UserSkillSerializer, PostSerializer, 
    EndorsementSerializer
)

# --- Permissions ---

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an 'user' attribute (like SkillProfile).
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the profile.
        if hasattr(obj, 'user'):
             return obj.user == request.user
        elif hasattr(obj, 'author'):
             return obj.author == request.user
        # For UserSkill/Endorsement, we need more specific checks in the ViewSet

        return False

# --- ViewSets ---

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Skills to be viewed. No creation/update allowed via API.
    """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    search_fields = ['name']
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Custom action for fast skill search.
        """
        query = request.query_params.get('q', '')
        if query:
            # Case-insensitive search starting with the query
            skills = self.queryset.filter(name__icontains=query)[:10] 
        else:
            skills = self.queryset.all()[:10]
            
        serializer = self.get_serializer(skills, many=True)
        return Response(serializer.data)


class SkillProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user profiles to be viewed or edited.
    """
    queryset = SkillProfile.objects.all()
    serializer_class = SkillProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    lookup_field = 'user__username' # Allows lookup via /profiles/username/

    def get_queryset(self):
        # Optionally filter or limit profiles here
        return self.queryset.select_related('user')

    def retrieve(self, request, *args, **kwargs):
        """
        Custom retrieve to handle the case where a profile might not exist for a user.
        """
        try:
            instance = self.get_object()
        except Exception:
            # Handle user not found or profile not created yet
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        # Ensure only the profile fields are updated, not the user object itself
        serializer.save()


class UserSkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing the skills listed on a user's profile (UserSkill cards).
    """
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Only show skills belonging to the current user's profile
        if self.request.user.is_authenticated:
            return UserSkill.objects.filter(profile__user=self.request.user)
        return UserSkill.objects.none()

    def perform_create(self, serializer):
        # Automatically link the new UserSkill to the current user's profile
        profile, created = SkillProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)

    def get_permissions(self):
        # Check that the user is the profile owner for update/destroy actions
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()


class EndorsementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating and viewing endorsements.
    """
    serializer_class = EndorsementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Allow viewing endorsements given by the user or received by the user
        if self.request.user.is_authenticated:
            return Endorsement.objects.filter(
                endorser=self.request.user
            ) | Endorsement.objects.filter(
                skill_card__profile__user=self.request.user
            ).select_related('skill_card__skill', 'skill_card__profile__user')
        return Endorsement.objects.none()

    def perform_create(self, serializer):
        # Automatically set the endorser to the currently logged-in user
        serializer.save(endorser=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and creating posts/status updates.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the author to the currently logged-in user
        serializer.save(author=self.request.user)
        
    @action(detail=False, methods=['get'])
    def user_feed(self, request):
        """
        Custom action to fetch posts for the authenticated user's feed.
        (For simplicity, currently just returns all posts, but later can be customized to follow logic).
        """
        # A simple feed: latest posts for now. In a real app, this would involve 'following' logic.
        posts = self.queryset.all().order_by('-created_at')[:50]
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)