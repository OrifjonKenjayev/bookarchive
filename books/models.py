# from django.db import models
# from django.utils.text import slugify


# class Category(models.Model):
#     name = models.CharField(max_length=120)
#     slug = models.SlugField(max_length=140, unique=True, blank=True)


#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.name)
#         super().save(*args, **kwargs)


#     def __str__(self):
#         return self.name


# class SubCategory(models.Model):
#     category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
#     name = models.CharField(max_length=120)
#     slug = models.SlugField(max_length=140, unique=True, blank=True)


#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(f"{self.category.name}-{self.name}")
#         super().save(*args, **kwargs)


#     def __str__(self):
#         return f"{self.category.name} > {self.name}"


# class Book(models.Model):
#     title = models.CharField(max_length=250)
#     author = models.CharField(max_length=200, blank=True)
#     description = models.TextField(blank=True)
#     category = models.ForeignKey(Category, related_name='books', on_delete=models.SET_NULL, null=True)
#     subcategory = models.ForeignKey(SubCategory, related_name='books', on_delete=models.SET_NULL, null=True, blank=True)
#     file = models.FileField(upload_to='books/files/')
#     cover = models.ImageField(upload_to='covers/', blank=True, null=True)  # <-- new field
#     uploaded_at = models.DateTimeField(auto_now_add=True)


#     def __str__(self):
#         return self.title











from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    cover = models.ImageField(upload_to='category_covers/', blank=True, null=True)  # New: For category covers/icons

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    cover = models.ImageField(upload_to='subcategory_covers/', blank=True, null=True)  # New: For subcategory covers/icons

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.category.name}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.category.name} > {self.name}"

class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='books', on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, related_name='books', on_delete=models.SET_NULL, null=True, blank=True)
    file = models.FileField(upload_to='books/files/')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)  # Already present: For book covers
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title