from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Account(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["code"]
        indexes = [models.Index(fields=["code"])]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        if self.pk:
            original = Account.objects.get(pk=self.pk)
            if original.name != self.name:
                raise ValidationError(
                    "El nombre de la cuenta es inmutable y no puede cambiarse.")
        super().save(*args, **kwargs)


class CostCenter(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    accounts = models.ManyToManyField(
        Account, through="CostCenterAccount",
        related_name="cost_centers",
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class CostCenterAccount(models.Model):

    cost_center = models.ForeignKey(CostCenter, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cost_center", "account"],
                name="uniq_costcenter_account",
            )
        ]
        indexes = [
            models.Index(fields=["cost_center", "account"]),
            models.Index(fields=["account"]),
        ]
        ordering = ["cost_center__code", "account__code"]

    def __str__(self):
        return f"{self.cost_center.name} - {self.account.name}"


class AnnualBudget(models.Model):
    cost_center_account = models.ForeignKey(
        CostCenterAccount, on_delete=models.CASCADE,
        related_name="annual_budgets")
    year = models.PositiveIntegerField()
    budget_amount = models.DecimalField(
        max_digits=16, decimal_places=2, default=0)
    executed_amount = models.DecimalField(
        max_digits=16, decimal_places=2, default=0)
    available_amount = models.DecimalField(
        max_digits=16, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("cost_center_account", "year")]
        ordering = ["-year", "cost_center_account__cost_center__code",
                    "cost_center_account__account__code"]
        indexes = [
            models.Index(fields=["year"]),
            models.Index(fields=["cost_center_account", "year"]),
        ]

    def __str__(self):
        cca = self.cost_center_account
        return f"{cca.cost_center.name} - {cca.account.name} - {self.year}"


class AdjustmentModel(models.Model):
    cost_center_account = models.ForeignKey(
        CostCenterAccount, on_delete=models.CASCADE)

    calculated_amount = models.DecimalField(
        max_digits=18, decimal_places=2, default=0)

    adjustment = models.DecimalField(
        max_digits=18, decimal_places=2, default=0)
    final_amount = models.DecimalField(
        max_digits=18, decimal_places=2, default=0)
    justification = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.cost_center_account.cost_center.name} - {self.cost_center_account.account.name}"
