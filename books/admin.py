# from django.contrib import admin
# from .models import Category, SubCategory, Book


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug')
#     prepopulated_fields = {'slug': ('name',)}


# @admin.register(SubCategory)
# class SubCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'slug')
#     prepopulated_fields = {'slug': ('name',)}


# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'category', 'subcategory', 'uploaded_at')
#     list_filter = ('category', 'subcategory')
#     search_fields = ('title', 'author')



from django.contrib import admin
from .models import Category, SubCategory, Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'slug', 'cover')  # Add cover here

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    fields = ('category', 'name', 'slug', 'cover')  # Add cover here

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'subcategory', 'uploaded_at')
    list_filter = ('category', 'subcategory')
    search_fields = ('title', 'author')
    fields = ('title', 'author', 'description', 'category', 'subcategory', 'file', 'cover')  # Add cover here (already in model)