from django.contrib import admin
from .models import AnnualBudget, CostCenterAccount, CostCenter, Account, AdjustmentModel

admin.site.register(AnnualBudget)


class AnnualBudgetInline(admin.TabularInline):
    model = AnnualBudget
    extra = 1
    fields = ("year", "budget_amount", "executed_amount",
              "available_amount", "notes")
    ordering = ("-year",)


class CostCenterAccountInline(admin.TabularInline):
    model = CostCenterAccount
    extra = 1
    autocomplete_fields = ("account",)


@admin.register(CostCenter)
class CostCenterAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    search_fields = ("code", "name")
    list_filter = ("is_active",)
    inlines = [CostCenterAccountInline]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(CostCenterAccount)
class CostCenterAccountAdmin(admin.ModelAdmin):
    list_display = ("cost_center", "account")
    search_fields = ("cost_center__code", "cost_center__name",
                     "account__code", "account__name")
    list_select_related = ("cost_center", "account")


@admin.register(AdjustmentModel)
class AdjustmentModelAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista del admin
    list_display = (
        "cost_center_account",
        "calculated_amount",
        "adjustment",
        "final_amount",
        "updated_at",
    )

    # Campos que serán buscables desde la barra superior
    search_fields = (
        "cost_center_account",
    )

    # Filtros laterales (opcional, pero útil)
    list_filter = (
        "cost_center_account",
    )

    # Orden por defecto
    ordering = ("cost_center_account",)

    # Campos de solo lectura (útil si no deben modificarse desde el admin)
    readonly_fields = ("created_at", "updated_at")

    # Configura el número de resultados por página
    list_per_page = 25
