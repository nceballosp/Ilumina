from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, TemplateView, CreateView, View
from .forms import RegisterForm
from django.contrib import messages
from .mixins import SuperUserRequiredMixin
from .models import AnnualBudget, AdjustmentModel, CostCenterAccount
from django.http import HttpRequest
from .utils.load import load_file
from .utils.budget import get_budget, final_budget
from django.db.models import Max
import json


class HomeView(TemplateView):
    template_name = 'home.html'


class LoadFileView(SuperUserRequiredMixin, TemplateView):
    template_name = 'load.html'

    def post(self, request: HttpRequest):
        file = request.FILES.get('data')
        year = request.POST.get('year')
        if str(file).split('.')[1] != 'xlsx':
            return JsonResponse({"detail": "El archivo tiene que ser un xlsx"},
                                status=400)
        if not file:
            return JsonResponse({"detail": "No se recibió archivo"},
                                status=400)
        df = load_file(file, year)
        if df:
            return JsonResponse({"detail": f"Archivo '{file.name}' cargado correctamente"})
        elif not df:
            return JsonResponse({"detail": f"Algo salio mal cargando los datos, revisar formato del archivo"})


class UpdateRowView(View):
    def put(self):
        pass


class BudgetAdjustmentView(LoginRequiredMixin, TemplateView):
    template_name = 'adjust_budget.html'


class BudgetAdjustmentTableView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        registers = AdjustmentModel.objects.values(
            "id",
            "cost_center_account__cost_center__name",
            "cost_center_account__cost_center__code",
            "cost_center_account__account__name",
            "cost_center_account__account__code",
            "calculated_amount",
            "adjustment",
            "final_amount",
            "justification",
        )

        return JsonResponse(list(registers), status=200, safe=False)


class SaveBudgetAdjustmentView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            # Parsear cuerpo JSON enviado desde Tabulator
            data = json.loads(request.body)

            if not isinstance(data, list) or not data:
                return JsonResponse(
                    {"detail": "No se recibieron datos válidos para guardar."},
                    status=400
                )

            # Opcional: limpiar registros anteriores
            AdjustmentModel.objects.all().delete()

            # Construir lista de objetos
            registers = [
                AdjustmentModel(
                    cost_center_account=CostCenterAccount.objects.get(
                        cost_center__code=row.get('cc_code'), account__code=row.get('acc_code')),
                    calculated_amount=row.get("calculated_amount") or 0
                )
                for row in data
                if row.get("cc_code") and row.get("cc_name")
            ]

            # Guardar en bulk para eficiencia
            AdjustmentModel.objects.bulk_create(registers)

            return JsonResponse({
                "detail": f"Se guardaron {len(registers)} registros correctamente"
            })

        except json.JSONDecodeError:
            return JsonResponse(
                {"detail": "Error al decodificar JSON recibido."},
                status=400
            )

        except Exception as e:
            return JsonResponse(
                {"detail": f"Error al guardar la tabla: {str(e)}"},
                status=500
            )


class UpdateBudgetAdjustmentView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            if not data:
                return JsonResponse({"detail": "No se recibieron datos."}, status=400)

            for row in data:
                AdjustmentModel.objects.filter(id=row.get("id")).update(
                    adjustment=row.get("adjustment"),
                    final_amount=final_budget(
                        row.get("calculated_amount"), row.get("adjustment")),
                    justification=row.get("justification")
                )

            return JsonResponse({"detail": "Cambios guardados correctamente"})
        except Exception as e:
            return JsonResponse({"detail": f"Error al guardar los cambios: {str(e)}"}, status=400)


class BudgetTableView(SuperUserRequiredMixin, TemplateView):
    template_name = 'budget.html'

    def post(self, request: HttpRequest):
        ipc: float = float(request.POST.get('ipc', 0))
        df: list = get_budget(ipc)
        if df:
            return JsonResponse(data=df, status=200, safe=False)


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginUserView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class LogoutUserView(LogoutView):
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Has cerrado sesión correctamente.")
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = 'api.has_portal_access'
    raise_exception = True
    template_name = 'dashboard.html'


class NegativeAccountReportView(SuperUserRequiredMixin, ListView):
    template_name = 'report.html'
    model = AnnualBudget
    context_object_name = 'data'

    def get_queryset(self):
        queryset = super().get_queryset()
        last_year = queryset.aggregate(Max('year')).get('year__max')
        queryset = queryset.filter(executed_amount__lt=0, year=last_year)
        return list(queryset.values('cost_center_account__cost_center__code', 'cost_center_account__cost_center__name', 'cost_center_account__account__name', 'cost_center_account__account__code', 'executed_amount', 'year'))


class CoordinatorPortalView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'api.has_portal_access'
    raise_exception = True
    template_name = 'coordinator_portal.html'
    model = AdjustmentModel
    context_object_name = 'data'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            cost_center_account__cost_center__user=self.request.user)
        return list(queryset.values('cost_center_account__cost_center__code', 'cost_center_account__cost_center__name', 'cost_center_account__account__name', 'cost_center_account__account__code', 'adjustment', 'calculated_amount', 'justification', 'final_amount'))
