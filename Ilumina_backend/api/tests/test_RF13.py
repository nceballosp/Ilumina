import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
from django.test import Client
from selenium.webdriver.support.ui import Select
from ..models import AnnualBudget,CostCenterAccount,CostCenter,Account
from urllib.parse import urlparse

'''TEST RF13: Visualización cuentas negativas.'''

class TabulatorFilterNegativeAccountTests(StaticLiveServerTestCase):

    """
    Prueba funcional para verificar que los filtros de Tabulator funcionan correctamente
    al aplicarse a cuentas con executed_amount negativo
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Usa Chrome, pero puedes cambiar por Firefox o Edge
        cls.username = "testuser"
        cls.password = "testpass123"
        cls.user = User.objects.create_superuser(
            username=cls.username, password=cls.password)

        # Setup objetos test para la tabla
        cc = CostCenter.objects.create(code='200', name='cc_name')
        acc = Account.objects.create(code='acc_code', name='acc_name')
        ccac = CostCenterAccount.objects.create(cost_center=cc, account=acc)
        ab = AnnualBudget.objects.create(cost_center_account=ccac, year=2025, budget_amount=10000,
                                         executed_amount=1000, available_amount=19999)
        cc2 = CostCenter.objects.create(code='100', name='cc_name2')
        acc2 = Account.objects.create(code='acc_code2', name='acc_name2')
        ccac2 = CostCenterAccount.objects.create(cost_center=cc2, account=acc2)
        ab2 = AnnualBudget.objects.create(cost_center_account=ccac2, year=2025, budget_amount=10000,
                                          executed_amount=1000, available_amount=19999)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # sin interfaz gráfica
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

    def setUp(self):
        # Crear un cliente de pruebas de Django y loguear para obtener la cookie de sesión
        client = Client()
        logged_in = client.login(
            username=self.username, password=self.password)
        assert logged_in, "No se pudo loguear el cliente de test; revisa las credenciales."

        # obtener el valor de sessionid del test client
        session_cookie = client.cookies.get("sessionid")
        assert session_cookie is not None, "No se encontró cookie 'sessionid' en client.cookies."

        # Navegar a la URL base para poder inyectar cookie en el dominio correcto
        parsed = urlparse(self.live_server_url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"
        self.driver.get(base_url)

        # Añadir la cookie de Django al navegador Selenium
        cookie_dict = {
            "name": "sessionid",
            "value": session_cookie.value,
            "path": "/",
            "domain": parsed.hostname,
        }
        try:
            self.driver.add_cookie(cookie_dict)
        except Exception:
            cookie_dict.pop("domain", None)
            self.driver.add_cookie(cookie_dict)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def test_tabulator_filters_work_negative_executed(self):
        """
        Verifica que al aplicar un filtro, el número de filas visibles disminuya.
        """
        # === 1. Ir a la página con la tabla ===
        url = f"{self.live_server_url}/generate_budget/"
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)
        ipc_input = self.driver.find_element(By.ID, 'ipc')
        ipc_input.send_keys('4.8')
        generate_button = self.driver.find_element(
            By.CSS_SELECTOR, '#generate-button')
        generate_button.click()
        # Esperar a que Tabulator esté cargado
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#table")))
        time.sleep(1)  # pequeño delay para asegurar renderizado
        # === 2. Contar filas antes del filtro ===
        rows_before = self.driver.find_elements(
            By.CSS_SELECTOR, ".tabulator-row")
        self.assertGreater(len(rows_before), 0,
                           "No hay filas iniciales en la tabla")

        print(f"➡️ Filas antes del filtro: {len(rows_before)}")

        # === 3. Aplicar un filtro ===
        # Opción 1: filtro global

        field_input = self.driver.find_element(By.CSS_SELECTOR, "#filter-field")
        type_input = self.driver.find_element(By.CSS_SELECTOR, "#filter-type")
        # Seleccionar el campo ejecucion y la relacion <
        dropdown_field = Select(field_input)
        dropdown_type = Select(type_input)
        dropdown_type.select_by_value('<')
        dropdown_field.select_by_value('Ejecucion_2025')
        search_input = self.driver.find_element(By.CSS_SELECTOR, "#filter-value")
        search_input.send_keys("0" + Keys.ENTER)
        time.sleep(1)
    
        # === 4. Contar filas después del filtro ===
        rows_after = self.driver.find_elements(
            By.CSS_SELECTOR, ".tabulator-row")

        print(f"➡️ Filas después del filtro: {len(rows_after)}")

        # === 5. Afirmación principal ===
        self.assertLess(
            len(rows_after),
            len(rows_before),
            "El filtro no redujo el número de filas visibles"
        )
        print("✅ El filtro redujo correctamente las filas visibles")
        for row in rows_after:
            executed_amount = row.find_element(By.CSS_SELECTOR,"div[tabulator-field='executed_amount']").text
            self.assertLessEqual(int(executed_amount.replace('.','')),0,'El valor ejecutado no es < a 0 ❌')
        print('Todas las filas mostradas tienen valores ejecutados negativos ✅')