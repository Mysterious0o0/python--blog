from django.contrib import admin

# Register your models here.
from .models import Category,Post,Tag

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','modified_time','category','author']
    

admin.site.register(Category)
admin.site.register(Post,PostAdmin)
admin.site.register(Tag)
