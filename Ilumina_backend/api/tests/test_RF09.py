import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User,Permission
from django.test import Client
from selenium.webdriver.support.ui import Select
from ..models import AnnualBudget,CostCenterAccount,CostCenter,Account,AdjustmentModel
from urllib.parse import urlparse
from django.contrib.contenttypes.models import ContentType

'''TEST RF09: Acceso desde portal.'''

class PortalAccessTests(StaticLiveServerTestCase):
    """Prueba funcional: un usuario del grupo 'contador' puede acceder al /portal/ desde la navbar."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Configurar Selenium (Chrome headless)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        # Crear grupo y usuario de prueba
        content_type = ContentType.objects.get_for_model(AdjustmentModel)
        portal_permission, _ = Permission.objects.get_or_create(name="Portal Access", codename="has_portal_access",content_type=content_type)
        self.username = "contador_user"
        self.password = "testpass123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.user_permissions.add(portal_permission)

        # Loguear al usuario y obtener cookie de sesión
        client = Client()
        client.login(username=self.username, password=self.password)
        session_cookie = client.cookies["sessionid"]

        # Preparar cookie para Selenium
        parsed = urlparse(self.live_server_url)
        self.driver.get(self.live_server_url)
        cookie = {
            "name": "sessionid",
            "value": session_cookie.value,
            "path": "/",
            "domain": parsed.hostname,
        }
        try:
            self.driver.add_cookie(cookie)
        except Exception:
            cookie.pop("domain", None)
            self.driver.add_cookie(cookie)

    def test_contador_can_access_portal(self):
        """El usuario con grupo contador ve y puede usar el enlace al portal."""
        wait = WebDriverWait(self.driver, 10)

        # 1️⃣ Ir a la página principal
        self.driver.get(f"{self.live_server_url}/")
        print("Visitando:", self.driver.current_url)

        # 2️⃣ Verificar que el botón/enlace del portal aparece en la navbar
        try:
            portal_link = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a[href='/portal/']")
                )
            )
        except Exception:
            self.fail("❌ No se encontró el enlace a /portal/ en la navbar.")

        print("✅ Enlace al portal encontrado en la navbar.")
        print("Visible?", portal_link.is_displayed())
        # 3️⃣ Hacer clic en el enlace
        portal_link.click()

        # 4️⃣ Esperar que cargue la página /portal/
        wait.until(EC.url_contains("/portal/"))
        current_url = self.driver.current_url
        print("➡️ Redirigido a:", current_url)

        # 5️⃣ Verificar contenido esperado (ajusta según tu portal.html)
        try:
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#table"))
            )
        except Exception:
            self.fail("❌ Se llegó a /portal/ pero el contenido esperado no apareció.")

        print("✅ El usuario contador pudo acceder correctamente al portal y se muestra correctamente la tabla.")
