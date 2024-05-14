from .scraping_vinculo import *
from django.conf import settings

SELENIUM_OPTIONS = settings.SELENIUM_OPTIONS

def buscar_vinculos(cpf):
    scraping = ScrapingVinculos(SELENIUM_OPTIONS['REMOTE_SELENIUM_ADDRESS'],
                                SELENIUM_OPTIONS['SELENIUM_REQUESTS_PROXY_HOST'])

    vinculo = scraping.buscar_vinculos(cpf)
    scraping.fechar_driver()

