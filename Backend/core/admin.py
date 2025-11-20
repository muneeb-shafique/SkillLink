from django.contrib import admin
from .models import Skill, SkillProfile, UserSkill, Post, Endorsement

# Register your models here.

# Customize how the Skill model appears in the admin
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Customize how the SkillProfile model appears
@admin.register(SkillProfile)
class SkillProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location')
    search_fields = ('user__username', 'location')

# Customize how UserSkill (the card that gets endorsed) appears
@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('profile', 'skill', 'self_rating', 'is_public')
    list_filter = ('is_public', 'skill')
    search_fields = ('profile__user__username', 'skill__name')
    raw_id_fields = ('profile', 'skill') # For selecting related objects efficiently

# Customize Posts
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'related_skill', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'content')
    raw_id_fields = ('author', 'related_skill')

# Customize Endorsements
@admin.register(Endorsement)
class EndorsementAdmin(admin.ModelAdmin):
    list_display = ('endorser', 'skill_card', 'endorser_rating', 'endorsed_at')
    list_filter = ('endorsed_at',)
    raw_id_fields = ('endorser', 'skill_card')