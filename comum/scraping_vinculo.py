from datetime import datetime, timedelta
from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumrequests import Remote

from .models import Profissional, Vinculo


class ScrapingVinculos:
    def __init__(self, remote_selenium_address, proxy_host):
        options = ChromeOptions()
        self.driver = Remote(
            command_executor=remote_selenium_address,
            options=options,
            proxy_host=proxy_host,
        )
        self.vinculos = {}

    def fechar_driver(self):
        self.driver.quit()

    def buscar_vinculos(self, cpf):
        profissional, created = Profissional.objects.get_or_create(cpf=cpf)
        if not created:
            return None


        self.driver.get('https://cnes.datasus.gov.br/pages/profissionais/consulta.jsp')
        campo_de_busca = self.driver.find_element('id', 'pesquisaValue')
        campo_de_busca.send_keys(cpf)
        campo_de_busca.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(5)

        try:
            self.driver.find_element('xpath', "//strong[contains(text(), 'Não Existem Dados para a Pesquisa Solicitada.')]")
            return
        except NoSuchElementException:
            pass
        sleep(0.5)
        self.busca_vinculos_ativos(profissional)
        sleep(0.5)
        self.driver.find_element('xpath', "//button[@class='btn btn-primary' and text()='Fechar']").click()
        sleep(0.5)
        self.buscar_historico_vinculos(profissional)

        for chave, valor in self.vinculos.items():
            Vinculo.objects.create(
                profissional=profissional,
                competencia=chave.split('-')[2],
                cnes=chave.split('-')[1],
                cbo=valor
            )

        return None

    def busca_vinculos_ativos(self, profissional):
        try:
            tabela = self.driver.find_element(by='css selector',
                                              value='table.table.table-bordered.table-striped.table-condensed.ng'
                                                    '-scope.ng'
                                                    '-table')
            botao_ativos = tabela.find_element(by='css selector',
                                               value='button.btn.btn-default[ng-click="pesquisaVinculos(prof.id)"]['
                                                     'title="Vínculos ativos"]')
            botao_ativos.click()

            self.driver.implicitly_wait(5)
            modal = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, 'vinculoModal'))
            )
            tabela_html = modal.find_element(by='id', value='relatorioGeralField').get_attribute('innerHTML')
            soup = BeautifulSoup(tabela_html, 'html.parser')
            linhas = soup.find_all('tr')

            dados_profissional = linhas[1].find_all('td')
            profissional.nome = dados_profissional[0].text
            profissional.cns = dados_profissional[1].text
            profissional.save()

            for linha in linhas[3: len(linhas) - 1]:
                dados_vinculo = linha.find_all('td')
                competencia = competencia_atual()
                chave = f"{profissional.cpf}-{dados_vinculo[4].text}-{competencia}"
                valor = dados_vinculo[3].text
                self.vinculos[chave] = valor
        except TimeoutException as e:
            print(f"Erro ao bsucar vinculos ativos: {e}")
            return

    def buscar_historico_vinculos(self, profissional):
        try:
            tabela = self.driver.find_element(by='css selector',
                                              value='table.table.table-bordered.table-striped.table-condensed.ng'
                                                    '-scope.ng'
                                                    '-table')
            botao_historico = tabela.find_element(by='css selector',
                                                  value='button.btn.btn-default[ng-click="historicoProfissional('
                                                        'prof.id)"]')
            botao_historico.click()

            self.driver.implicitly_wait(5)
            # Esperar pelo modal carregar
            modal = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.ID, 'historicoProfissionalModal'))
            )
            tabela_html = modal.find_element(by='css selector',
                                             value='table.table.table-bordered.table-striped.table-condensed').get_attribute(
                'innerHTML')
            soup = BeautifulSoup(tabela_html, 'html.parser')
            linhas = soup.find_all('tr')

            dados_profissional = linhas[1].find_all('td')
            profissional.nome = dados_profissional[0].text
            profissional.cns = dados_profissional[1].text
            profissional.save()

            for linha in linhas[3:]:
                dados_vinculo = linha.find_all('td')

                chave = f"{profissional.cpf}-{dados_vinculo[5].text}-{dados_vinculo[0].text}"
                valor = dados_vinculo[4].text
                self.vinculos[chave] = valor
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Erro ao bsucar vinculos ativos: {e}")


def competencia_atual():
    data_atual = datetime.now()

    mes_anterior = data_atual - timedelta(days=data_atual.day)

    return mes_anterior.strftime("%m/%Y")
