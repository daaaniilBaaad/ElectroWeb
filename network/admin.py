from django.contrib import admin
from .models import NetworkNode, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt_to_supplier=0)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ["name", "level", "city", "country", "debt_to_supplier", "created_at"]
    list_filter = ["city", "country"]
    search_fields = ["name", "city"]
    inlines = [ProductInline]
    actions = [clear_debt]

    fieldsets = [
        (None, {
            "fields": ["name", "supplier", "debt_to_supplier"]
        }),
        ("Контакты", {
            "fields": ["email", "country", "city", "street", "house_number"]
        }),
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["created_at", "level"]
        return ["created_at"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "model", "release_date", "network_node"]
    list_filter = ["release_date"]
    search_fields = ["name", "model"]
