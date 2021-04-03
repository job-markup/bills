from django.contrib import admin

from .models import Product, ShopInfo, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'product_code', 'stock', 'price', 'created_at']
    list_filter = ['product_code', 'created_at']
    list_editable = ['price', 'stock']
    ordering = ['-created_at']


@admin.register(ShopInfo)
class ShopInfoAdmin(admin.ModelAdmin):
    list_display = ['__str__']

    def has_add_permission(self, request):  # Limited the add to 1
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):  # Prevented deletion
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at', 'updated_at']
    readonly_fields = ['slug']
    list_filter = ['created_at', 'updated_at']
    ordering = ['-created_at']
