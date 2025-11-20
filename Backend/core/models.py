from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

# --- Core Skill Definitions ---

class Skill(models.Model):
    """
    A foundational model for all available skills (e.g., 'Python', 'Leadership', 'Cooking').
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


# --- Profile & User Skills ---

class SkillProfile(models.Model):
    """
    User-specific profile information linked one-to-one with the built-in Django User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    profile_picture_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"


class UserSkill(models.Model):
    """
    Represents a specific skill claimed by a user on their profile (the item that gets endorsed).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(SkillProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    
    # User's self-assessment of their skill level (1-5)
    self_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=1,
    )
    is_public = models.BooleanField(default=True)

    class Meta:
        unique_together = ('profile', 'skill')
        ordering = ['skill__name']
        verbose_name_plural = "User Skills"

    def __str__(self):
        return f"{self.profile.user.username}'s {self.skill.name}"


# --- Interaction & Social Features ---

class Post(models.Model):
    """
    A simple status update or microblog post from a user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    related_skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.author.username}"


class Endorsement(models.Model):
    """
    Represents an endorsement given by one user to another user's skill (UserSkill).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    endorser = models.ForeignKey(User, related_name='given_endorsements', on_delete=models.CASCADE)
    skill_card = models.ForeignKey(UserSkill, related_name='endorsements', on_delete=models.CASCADE)
    
    comment = models.TextField(blank=True, null=True)
    
    endorser_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True
    )
    endorsed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('endorser', 'skill_card')
        ordering = ['-endorsed_at']

    def __str__(self):
        return f"Endorsement for {self.skill_card.profile.user.username}'s {self.skill_card.skill.name}"