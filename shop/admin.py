from django.contrib import admin
from shop.models import *
from django.contrib.auth.models import User, Group


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_appropriate')
    list_filter = ('created_at', 'email')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def product_count(self, obj):
        return obj.products.count()
    list_display = ('title', 'slug', 'product_count')
    # prepopulated_fields = {'slug': ('title',)}
    fields = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def comment_count(self, obj):
        return obj.comments.count()

    def order_count(self, obj):
        return obj.orders.count()

    list_display = ('name', 'price', 'quantity', 'comment_count', 'order_count')
    list_filter = ('category_id', )
    prepopulated_fields = {"slug": ('name',)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'quantity')
    list_filter = ['email', ]


#
# admin.site.register(Product, ProductAdmin)
admin.site.unregister(User)
admin.site.unregister(Group)

# Register your models here.
