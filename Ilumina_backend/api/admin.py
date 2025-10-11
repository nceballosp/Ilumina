from django.contrib import admin
from .models import AnnualBudget, CostCenterAccount, CostCenter, Account

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
