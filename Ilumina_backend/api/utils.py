import pandas as pd
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import CostCenter, CostCenterAccount, Account, AnnualBudget


def load_table(file):
    table = pd.read_excel(file, sheet_name='Presupuesto completo').fillna(0)
    for index, row in table.iterrows():
        cost_center_row, created = CostCenter.objects.get_or_create(
            name=row['Nombre Centro de costo'], code=row['Centro de costo'])
        account_row, created = Account.objects.get_or_create(
            name=row['Nombre cuenta'], code=row['Cuenta contable'])
        print(cost_center_row)
        print(account_row)
    # temporalmente retorna el dataframe completo
    # TO DO: Cambiar retorno a query o True si cargo todos los objetos a la db correctamente
    return table.to_dict(orient='records')


if __name__ == '__main__':
    load_table('2026.xlsx')
