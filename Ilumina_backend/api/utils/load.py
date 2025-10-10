
import pandas as pd
import numpy as np
import re, json
from django.db import transaction
from ..models import *

def _norm_text(val: str) -> str:
    if val is None:
        return ""
    s = str(val).strip()
    # Colapsa espacios múltiples
    s = re.sub(r"\s+", " ", s)
    return s

def _norm_code(val) -> str:
    """
    Convierte códigos de Excel a string fiable:
    - Mantiene ceros a la izquierda
    - Elimina sufijo '.0' típico de floats
    - Quita espacios
    """
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return ""
    s = str(val).strip()
    # Si viene como float entero ("5195200001.0"), quita ".0"
    if re.fullmatch(r"\d+\.0", s):
        s = s[:-2]
    # Si es float con decimales raros, intenta formatear como entero cuando aplique
    try:
        f = float(s)
        if f.is_integer():
            s = str(int(f))
    except Exception:
        pass
    return s

def load_file(file):

    xls = pd.ExcelFile(file)
    sheet_names = xls.sheet_names
    table = pd.read_excel(
        file,
        sheet_name= sheet_names[0], #!!! Normalizar segun como venga de SIPRES
        dtype=str,
        keep_default_na=False,
    )

    # Columnas de códigos y nombres
    COL_CC_NAME = "Centro costos nombre"
    COL_CC_CODE = "Centro costos"
    COL_ACC_NAME = "Descripción cuenta"
    COL_ACC_CODE = "Cuenta"

    # Columnas de datos
    COL_BUDGET_AMOUNT = "Presupuesto actual"
    COL_EXECUTED_AMOUNT = "Ejecutado al periodo"
    COL_AVAILABLE_AMOUNT = "Disponible al periodo"

    YEAR = sheet_names[0]

    # Limpieza en bloque
    table[COL_CC_NAME] = table[COL_CC_NAME].map(_norm_text)
    table[COL_CC_CODE] = table[COL_CC_CODE].map(_norm_code)
    table[COL_ACC_NAME] = table[COL_ACC_NAME].map(_norm_text)
    table[COL_ACC_CODE] = table[COL_ACC_CODE].map(_norm_code)

    created_cc = created_acc = created_ccac = 0
    processed = 0

    for idx, row in table.iterrows():
        cc_code = row[COL_CC_CODE]
        cc_name = row[COL_CC_NAME]
        acc_code = row[COL_ACC_CODE]
        acc_name = row[COL_ACC_NAME]

        ba_amount = row[COL_BUDGET_AMOUNT]
        ea_amount = row[COL_EXECUTED_AMOUNT]
        aa_amount = row[COL_AVAILABLE_AMOUNT]

        # Salta filas sin códigos (clave)
        if not cc_code or not acc_code:
            continue

        cc, created = CostCenter.objects.get_or_create(code=cc_code, name=cc_name)
        if created:
            created_cc += 1

        acc, created = Account.objects.get_or_create(code=acc_code, name=acc_name)
        if created:
            created_acc += 1

        ccac, created = CostCenterAccount.objects.get_or_create(cost_center=cc, account=acc)
        if created:
            created_ccac += 1

        __, created = AnnualBudget.objects.get_or_create(cost_center_account=ccac, year=YEAR, budget_amount=ba_amount, executed_amount=ea_amount, available_amount=aa_amount)

        processed += 1

    print(f"Filas procesadas: {processed}")
    print(f"CostCenters creados: {created_cc}")
    print(f"Accounts creadas: {created_acc}")
    print(f"CostCenterAccounts creadas: {created_ccac}")

    return True



