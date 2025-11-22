from django.contrib import admin
from .models import Phone, Review, Wishlist, Comparison, UserProfile

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'id')
    search_fields = ('brand', 'model')
    list_filter = ('brand',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')

@admin.register(Comparison)
class ComparisonAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone1', 'phone2', 'created_at')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
