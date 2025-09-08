import pandas as pd
import numpy as np
import re
import json
from django.db import transaction
from ..models import *


def get_budget(ipc: float):

    qs = (AnnualBudget.objects
          .select_related("cost_center_account__cost_center", "cost_center_account__account")
          .all())

    # Convertimos a lista de dicts
    rows = []
    for ab in qs:
        rows.append({
            "cc_code": ab.cost_center_account.cost_center.code,
            "cc_name": ab.cost_center_account.cost_center.name,
            "acc_code": ab.cost_center_account.account.code,
            "acc_name": ab.cost_center_account.account.name,
            "year": ab.year,
            "budget": float(ab.budget_amount or 0),
            "executed": float(ab.executed_amount or 0),
            "available": float(ab.available_amount or 0),
        })

    df = pd.DataFrame(rows)
    # Pivot de budget
    df_budget = df.pivot_table(
        index=["cc_code", "cc_name", "acc_code", "acc_name"],
        columns="year",
        values="budget",
        fill_value=0
    )

    last_4 = sorted(df_budget.columns)[-4:]
    df_budget = df_budget[last_4]

    # Renombrar columnas → Presupuesto_20XX
    df_budget = df_budget.add_prefix("Presupuesto_").reset_index()
    last_year = df["year"].max()
    df_last = df[df["year"] == last_year][
        ["cc_code", "cc_name", "acc_code", "acc_name", "executed", "available"]
    ].rename(columns={
        "executed": f"Ejecucion_{last_year}",
        "available": f"Disponible_{last_year}",
    })

    # Merge budgets + últimos valores
    final_table = pd.merge(
        df_budget,
        df_last,
        on=["cc_code", "cc_name", "acc_code", "acc_name"],
        how="left"
    )

    # Ordenar columnas
    cols = ["cc_code", "cc_name", "acc_code", "acc_name"] + \
        sorted([c for c in final_table.columns if c.startswith("Presupuesto_")]) + \
        [f"Ejecucion_{last_year}", f"Disponible_{last_year}"]

    final_table = final_table[cols].rename(columns={
        "cc_code": "Centro de Costos",
        "cc_name": "Nombre Centro de Costos",
        "acc_code": "Cuenta Contable",
        "acc_name": "Nombre Cuenta",
    })
    last_4 = [f'Presupuesto_{year}' for year in last_4]
    final_table['Promedio 4 años'] = final_table[last_4].sum(axis=1)/4
    final_table['Presupuesto Calculado'] = round(final_table[f'Presupuesto_{last_year}'] *(1+(ipc/100)),0)

    json_str = final_table.to_json(orient="records", force_ascii=False)
    data = json.loads(json_str)
    return data
