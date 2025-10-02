from django.contrib import admin
from .models import Category, Customer, Product, Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
    model = Profile


# class UserAdmin(admin.ModelAdmin):
#     model = User
#     fields = []

class UserAdmin(DefaultUserAdmin):
    inlines = [ProfileInline,]
    

admin.site.unregister(User)
admin.site.register(User, UserAdmin)