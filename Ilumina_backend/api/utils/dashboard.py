import math
from ..models import AnnualBudget, CostCenter, User, CostCenterAccount
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
from plotly.subplots import make_subplots
from django.db.models import Sum, DecimalField, QuerySet, Max


def total_budget(user: User):
    last_year = AnnualBudget.objects.aggregate(
        fecha_max=Max("year"))["fecha_max"]
    cost_centers = CostCenter.objects.filter(user=user, costcenteraccount__annual_budgets__year=last_year).annotate(
        budget=Sum('costcenteraccount__annual_budgets__budget_amount'),
        executed=Sum('costcenteraccount__annual_budgets__executed_amount'))

    cost_centers = calculate_accomplishment(user, cost_centers.values(
        'id', 'name', 'budget', 'executed'))
    return cost_centers


def calculate_accomplishment(user: User, centers_info):
    for center in centers_info:
        percentage = (
            (center.get('budget') - center.get('executed')) / center.get('budget'))*100
        center['accomplishment'] = round(percentage, 2)

        center['budget'] = f"{round(center.get('budget'), 2):,}"
        center['executed'] = f"{round(center.get('executed'), 2):,}"

        data = get_data(user, center)
        chart = pie_charts(data)
        center['chart'] = chart

    return centers_info


def get_data(user: User, cost_center):
    last_year = AnnualBudget.objects.aggregate(
        fecha_max=Max("year"))["fecha_max"]
    budget_details = AnnualBudget.objects.filter(
        cost_center_account__cost_center__user=user,
        cost_center_account__cost_center=cost_center.get('id'),
        year=last_year
    ).values(
        'cost_center_account__cost_center__name',
        'cost_center_account__account__name',
    ).annotate(
        total_budget=Sum('budget_amount', output_field=DecimalField())
    ).order_by(
        'cost_center_account__cost_center__name',
        'cost_center_account__account__name'
    )

    data_for_df = []
    for item in budget_details:
        data_for_df.append({
            'name': item['cost_center_account__cost_center__name'],
            'account_name': item['cost_center_account__account__name'],
            'budget_amount': item['total_budget']
        })

    return data_for_df


def pie_charts(data: list):
    if not data:
        print("No hay datos para generar el gráfico.")
        return None

    df = pd.DataFrame(data)

    center_name = df['name'].iloc[0] if not df.empty else "Centro de Costos"

    fig = go.Figure(data=[
        go.Pie(
            labels=df['account_name'],
            values=df['budget_amount'],
            name=center_name,
            hovertemplate="<b>Cuenta:</b> %{label}<br><b>Monto:</b> %{value:$,.2f}<br><b>Porcentaje:</b> %{percent}<extra></extra>"
        )
    ])

    fig.update_traces(textposition='inside')

    fig.update_layout(
        height=600,
        width=800,
        showlegend=True,
        uniformtext_minsize=12,
        uniformtext_mode='hide'
    )

    return fig.to_html(full_html=False, include_plotlyjs='cdn')
