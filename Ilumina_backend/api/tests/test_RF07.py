import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
from django.test import Client
from ..models import AnnualBudget,CostCenterAccount,CostCenter,Account
from urllib.parse import urlparse

'''TEST RF07: Reporte cuentas en negativo.'''

class NegativeAccountReportTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Usa Chrome, pero puedes cambiar por Firefox o Edge
        cls.username = "testuser"
        cls.password = "testpass123"
        cls.user = User.objects.create_superuser(username=cls.username, password=cls.password)
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
            executed_amount=-1000, available_amount=19999)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # sin interfaz gráfica
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

    def setUp(self):
        # Crear un cliente de pruebas de Django y loguear para obtener la cookie de sesión
        client = Client()
        logged_in = client.login(username=self.username, password=self.password)
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
    def test_report_generated(self):
        url = f"{self.live_server_url}/report/"
        self.driver.get(url)
        time.sleep(2)
        rows = self.driver.find_elements(By.CSS_SELECTOR, ".tabulator-row")
        for row in rows:
            executed_amount = row.find_element(By.CSS_SELECTOR,"div[tabulator-field='executed_amount']").text
            self.assertLessEqual(int(executed_amount.replace('.','')),0,'El valor ejecutado no es < a 0 ❌')
        print('Todas las filas mostradas tienen valores ejecutados negativos ✅')
        wait = WebDriverWait(self.driver, 10)