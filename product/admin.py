from django.contrib import admin
from product.models import Product, Category
from review.models import Comment


admin.site.register(Category)


class CommentInLine(admin.TabularInline):
    model = Comment


class ProductAdmin(admin.ModelAdmin):
    list_filter = ['title', 'price', ]
    list_display = ['title', 'slug']
    search_fields = ['title', 'description']
    inlines = [CommentInLine]

admin.site.register(Product, ProductAdmin)