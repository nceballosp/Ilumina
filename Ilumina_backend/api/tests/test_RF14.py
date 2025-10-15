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

'''
TEST RF14: Gestión de usuarios.
'''