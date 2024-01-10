import warnings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
from .models import Profissional, Vinculo
from django.db import transaction

warnings.filterwarnings("ignore", category=FutureWarning)

def competencia_atual():
    data_atual = datetime.now()
    return data_atual.strftime("%m/%Y")

def busca_vinculos_ativos(driver, profissional):
    tabela = driver.find_element(by='css selector',
                                 value='table.table.table-bordered.table-striped.table-condensed.ng-scope.ng-table')
    botao_ativos = tabela.find_element(by='css selector',
                                       value='button.btn.btn-default[ng-click="pesquisaVinculos(prof.id)"][title="Vínculos ativos"]')
    botao_ativos.click()

    driver.implicitly_wait(5)
    modal = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'vinculoModal'))
    )
    tabela_html = modal.find_element(by='id', value='relatorioGeralField').get_attribute('innerHTML')
    soup = BeautifulSoup(tabela_html, 'html.parser')
    linhas = soup.find_all('tr')

    dados_profissional = linhas[1].find_all('td')
    profissional.nome = dados_profissional[0].text
    profissional.cns = dados_profissional[1].text
    profissional.save()

    vinculos = []
    for linha in linhas[3: len(linhas) -1]:
        dados_vinculo = linha.find_all('td')
        vinculo = Vinculo(
              profissional            = profissional
            , competencia             = competencia_atual()
            , ibge                    = dados_vinculo[0].text
            , uf                      = dados_vinculo[1].text
            , municipio               = dados_vinculo[2].text
            , cbo                     = dados_vinculo[3].text
            , cnes                    = dados_vinculo[4].text
            , cnpj                    = dados_vinculo[5].text
            , estabelecimento         = dados_vinculo[6].text
            , nat_juridica            = dados_vinculo[7].text
            , gestao                  = dados_vinculo[8].text
            , sus                     = dados_vinculo[9].text
            , vinculo_estabelecimento = dados_vinculo[13].text
            , vinculo_empregador      = dados_vinculo[14].text
            , detalhamento_vinculo    = dados_vinculo[15].text
            , ch_outros               = dados_vinculo[16].text
            , ch_ambulatorial         = dados_vinculo[17].text
            , ch_hospitalar           = dados_vinculo[18].text
            , preceptor               = dados_vinculo[10].text
            , residente               = dados_vinculo[11].text
            , desligamento            = dados_vinculo[12].text
        )
        vinculos.append(vinculo)
    return vinculos

def buscar_historico_vinculos(driver, profissional):
    # Localizar o botão de histórico
    tabela = driver.find_element(by='css selector',
                                 value='table.table.table-bordered.table-striped.table-condensed.ng-scope.ng-table')
    botao_historico = tabela.find_element(by='css selector',
                                          value='button.btn.btn-default[ng-click="historicoProfissional(prof.id)"]')
    botao_historico.click()

    driver.implicitly_wait(5)
    # Esperar pelo modal carregar
    modal = WebDriverWait(driver, 5).until(
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

    vinculos = []
    # construir os vinculos
    for linha in linhas[3:]:
        dados_vinculo = linha.find_all('td')
        vinculo = Vinculo(
              profissional            = profissional
            , competencia             = dados_vinculo[0].text
            , ibge                    = dados_vinculo[1].text
            , uf                      = dados_vinculo[2].text
            , municipio               = dados_vinculo[3].text
            , cbo                     = dados_vinculo[4].text
            , cnes                    = dados_vinculo[5].text
            , cnpj                    = dados_vinculo[6].text
            , estabelecimento         = dados_vinculo[7].text
            , nat_juridica            = dados_vinculo[8].text
            , gestao                  = dados_vinculo[9].text
            , sus                     = dados_vinculo[10].text
            , vinculo_estabelecimento = dados_vinculo[11].text
            , vinculo_empregador      = dados_vinculo[12].text
            , detalhamento_vinculo    = dados_vinculo[13].text
            , ch_outros               = dados_vinculo[14].text
            , ch_ambulatorial         = dados_vinculo[15].text
            , ch_hospitalar           = dados_vinculo[16].text
        )
        vinculos.append(vinculo)
    return vinculos


def buscar_vinculos(cpf):
    options = Options()
    options.add_argument("--headless")
    driver_1 = webdriver.Chrome(options=options,)
    driver_2 = webdriver.Chrome(options=options,)
    profissional, created = Profissional.objects.get_or_create(cpf=cpf)
    try:
        driver_1.get('https://cnes.datasus.gov.br/pages/profissionais/consulta.jsp')
        driver_2.get('https://cnes.datasus.gov.br/pages/profissionais/consulta.jsp')

        campo_busca_1 = driver_1.find_element('id', 'pesquisaValue')
        campo_busca_2 = driver_2.find_element('id', 'pesquisaValue')

        campo_busca_1.send_keys(cpf)
        campo_busca_1.send_keys(Keys.RETURN)
        campo_busca_2.send_keys(cpf)
        campo_busca_2.send_keys(Keys.RETURN)
        driver_1.implicitly_wait(5)
        driver_2.implicitly_wait(5)
        vinculos_ativos = busca_vinculos_ativos(driver_1, profissional)
        vinculos_historicos = buscar_historico_vinculos(driver_2, profissional)

        vinculos_ativos = [vinculo for vinculo in vinculos_ativos if not Vinculo.objects.filter(competencia=vinculo.competencia, cnes=vinculo.cnes,cbo=vinculo.cbo).exists()]
        vinculos_historicos = [vinculo for vinculo in vinculos_historicos if not Vinculo.objects.filter(competencia=vinculo.competencia, cnes=vinculo.cnes,cbo=vinculo.cbo).exists()]

        with transaction.atomic():
                Vinculo.objects.bulk_create(vinculos_ativos)
                Vinculo.objects.bulk_create(vinculos_historicos)

    except Exception as e:
        print(f"Erro ao buscar cbos: {e}")
        return None

