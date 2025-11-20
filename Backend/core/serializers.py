from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Skill, SkillProfile, UserSkill, Post, Endorsement

# --- Helper Serializers ---

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the basic Django User model, exposing only necessary fields.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class SkillSerializer(serializers.ModelSerializer):
    """
    Serializer for the base Skill model (e.g., 'Python', 'Leadership').
    """
    class Meta:
        model = Skill
        fields = ('id', 'name')

# --- Core Profile Serializers ---

class UserSkillSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserSkill card, showing the skill name and rating.
    """
    skill = SkillSerializer(read_only=True) # Nested serializer to show skill details

    class Meta:
        model = UserSkill
        fields = ('id', 'skill', 'self_rating', 'is_public')
        read_only_fields = ('profile',)


class SkillProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the SkillProfile model, including related user and skills.
    """
    user = UserSerializer(read_only=True)
    # Use the UserSkillSerializer to represent the skills listed on the profile
    listed_skills = UserSkillSerializer(source='userskill_set', many=True, read_only=True)

    class Meta:
        model = SkillProfile
        fields = ('user', 'bio', 'location', 'profile_picture_url', 'listed_skills')


# --- Interaction Serializers ---

class EndorsementSerializer(serializers.ModelSerializer):
    """
    Serializer for the Endorsement model.
    Handles creation and display of endorsements.
    """
    # Read-only fields for display
    endorser = UserSerializer(read_only=True)
    
    # Writable field: the ID of the UserSkill card being endorsed
    skill_card_id = serializers.PrimaryKeyRelatedField(
        queryset=UserSkill.objects.all(), 
        source='skill_card',
        write_only=True
    )
    
    # Read-only fields to display the endorsed skill and recipient
    recipient_username = serializers.CharField(source='skill_card.profile.user.username', read_only=True)
    endorsed_skill_name = serializers.CharField(source='skill_card.skill.name', read_only=True)

    class Meta:
        model = Endorsement
        fields = (
            'id', 'endorser', 'skill_card', 'skill_card_id', 
            'recipient_username', 'endorsed_skill_name',
            'comment', 'endorser_rating', 'endorsed_at'
        )
        read_only_fields = ('skill_card',) # Prevent direct writing to skill_card field

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.
    """
    author = UserSerializer(read_only=True)
    related_skill = SkillSerializer(read_only=True)
    
    # Writable field to link the post to a skill ID during creation/update
    related_skill_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(), 
        source='related_skill', 
        write_only=True,
        required=False
    )

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'related_skill', 'related_skill_id', 'created_at')
        read_only_fields = ('author',)