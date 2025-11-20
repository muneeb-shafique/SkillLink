from django.db import models
from django.contrib.auth.models import AbstractUser

# --- CHOICES ---
SKILL_LEVEL_CHOICES = [
    ('B', 'Beginner'),
    ('I', 'Intermediate'),
    ('A', 'Advanced'),
]

CONFIDENCE_CHOICES = [
    (1, 'Low'),
    (2, 'Moderate'),
    (3, 'Solid'),
    (4, 'High'),
    (5, 'Expert'),
]

# 1. The Custom User Model (SkillProfile)
# We extend the default Django user to add our skill-focused fields.
class SkillProfile(AbstractUser):
    """
    Custom User model including skill-specific attributes.
    This replaces the default Django User model.
    """
    # Standard field for a user's self-introduction
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text="A short description of yourself and your professional goals."
    )
    
    location = models.CharField(
        max_length=100,
        blank=True
    )

    # --- SkillLink Specific Fields ---
    
    # The one skill the user is currently highlighting or focusing on
    primary_skill = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="The main skill you want to be known for right now (e.g., 'React Development')."
    )

    # User's self-assessed level in their primary skill
    skill_level = models.CharField(
        max_length=1,
        choices=SKILL_LEVEL_CHOICES,
        default='B',
        help_text="Self-assessed level: Beginner, Intermediate, or Advanced."
    )

    def __str__(self):
        return self.username or "New User"


# 2. The Skill Model
class Skill(models.Model):
    """
    Defines a unique skill that can be tracked, endorsed, or learned.
    Supports a hierarchical structure (skill tree) via parent_skill.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the skill (e.g., Python, UI/UX Design, Public Speaking)."
    )
    
    category = models.CharField(
        max_length=50,
        help_text="The broad category this skill belongs to (e.g., Programming, Design, Communication)."
    )

    description = models.TextField(
        blank=True,
        help_text="Detailed description of what this skill entails."
    )

    # Self-referential ForeignKey for creating a skill hierarchy (e.g., 'Django' is a child of 'Python')
    parent_skill = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='sub_skills',
        help_text="The broader skill this skill belongs under (optional)."
    )

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.name


# 3. The Endorsement Model (The differentiator)
class Endorsement(models.Model):
    """
    Represents a skill validation from one user to another. This replaces simple 'likes'.
    """
    # The user giving the endorsement
    endorser = models.ForeignKey(
        SkillProfile, 
        on_delete=models.CASCADE, 
        related_name='given_endorsements',
        help_text="The user who is endorsing the skill."
    )
    
    # The user receiving the endorsement
    endorsee = models.ForeignKey(
        SkillProfile, 
        on_delete=models.CASCADE, 
        related_name='received_endorsements',
        help_text="The user receiving the endorsement."
    )
    
    # The specific skill being endorsed
    skill = models.ForeignKey(
        Skill, 
        on_delete=models.CASCADE, 
        related_name='endorsements',
        help_text="The specific skill being validated."
    )

    # How confident the endorser is in the user's ability (1-5 score)
    confidence_level = models.IntegerField(
        choices=CONFIDENCE_CHOICES,
        default=3,
        help_text="A score (1-5) indicating the endorser's confidence in the skill."
    )

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        # Ensures a user can only endorse another user for the SAME skill once.
        unique_together = ('endorser', 'endorsee', 'skill')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.endorser.username} endorses {self.endorsee.username} for {self.skill.name} ({self.get_confidence_level_display()})"