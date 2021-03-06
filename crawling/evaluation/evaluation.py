import requests
from threading import Thread
import urllib.robotparser
from datetime import datetime as dt

from crawling.occurrences import Occurrences
from crawling.recommendations import *


class Evaluation(Thread):
    """
    Conjunto de métodos para aplicação de Threads e avaliações para os sítios eletrônicos.
    """
    def __init__(self, city):
        Thread.__init__(self)
        self.city = city
        self.occurrences = Occurrences()
        self.sourcecode = None

    def run(self):
        self.validate_robots()

    def validate_robots(self):
        """
        Confere o arquivo robots.txt dos sites e verifica condições de Dissalow
        adicionando duas keys novas ao dict da cidade correspondente:
            - has_robotstxt (True/False): responde a pergunta se tem ou não o arquivo robots.txt
            - can_crawling (True/False): responde a pergunta se pode ou não fazer crawling
        """
        print(f'{self.city["city_name"]}: Verificação do arquivo robots.')

        try:
            self.city['timestamp'] = dt.timestamp(dt.now())
            self.city['has_robotstxt'] = False
            self.city['can_crawling'] = True

            city_url = self.city['url']
            city_url_robots = city_url + 'robots.txt'
            robotstxt = requests.get(city_url_robots, timeout=30, headers={'user-agent': 'uscs/0.0.1'})

            if robotstxt.status_code == 200:
                self.city['has_robotstxt'] = True
                robotparser = urllib.robotparser.RobotFileParser()
                robotparser.set_url(city_url_robots)
                robotparser.read()

                if not robotparser.can_fetch('*', city_url):
                    self.city['can_crawling'] = False
                    print(f'{self.city["city_name"]}: Sem permissão para fazer crawling.')

            if self.city['can_crawling']:
                self.sourcecode = self.get_sourcecode()
                self.validate_recommendations()

        except requests.exceptions.RequestException as error:
            print(dt.timestamp(dt.now()), self.city['_id'], self.city["city_name"], error)

    def get_sourcecode(self):
        """
        Faz requisição do código fonte da página inicial do sítio eletrônico.
        Se bem sucedido, guarda duas novas keys no dict da cidade correspondente:
            - timestamp: momento da requisição
            - sourcecode: conteúdo da resposta da requisição

        :return: <Response>.content OR None
        """
        print(f'{self.city["city_name"]}: Crawling do sourcecode.')

        try:
            self.sourcecode = requests.get(self.city['url'], timeout=30, headers={'user-agent': 'uscs/0.0.1'})

            if self.sourcecode.status_code == 200:
                return self.sourcecode.content

            return None

        except requests.exceptions.RequestException as error:
            print(dt.timestamp(dt.now()), self.city['_id'], self.city["city_name"], error)

    def validate_recommendations(self):
        """
        A partir do código fonte da página inicial do sítio eletrônico, valida as
        recomendações listadas e guarda suas ocorrências na lista de ocorrências.
        """
        print(f'{self.city["city_name"]}: Validação das recomendações.')

        if self.sourcecode is not None:
            rec03 = Recommendation03(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec03})
            rec06 = Recommendation06(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec06})
            rec07 = Recommendation07(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec07})
            rec08 = Recommendation08(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec08})
            rec09 = Recommendation09(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec09})
            rec11 = Recommendation11(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec11})
            rec16 = Recommendation16(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec16})
            rec17 = Recommendation17(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec17})
            rec19 = Recommendation19(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec19})
            rec20 = Recommendation20(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec20})
            rec23 = Recommendation23(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec23})
            rec24 = Recommendation24(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec24})
            rec26 = Recommendation26(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec26})
            rec31 = Recommendation31(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec31})
            rec33 = Recommendation33(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec33})
            rec34 = Recommendation34(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec34})
            rec36 = Recommendation36(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec36})
            rec38 = Recommendation38(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec38})
            rec39 = Recommendation39(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec39})
            rec44 = Recommendation44(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec44})

            rec16 = Recommendation16(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec16})
            rec17 = Recommendation17(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec17})
            rec23 = Recommendation23(self.sourcecode).avaliacao()
            self.occurrences.add({self.city['_id']: rec23})

            rec01_html = Recommendation01(self.sourcecode, url=self.city['url']).validar_html()
            self.occurrences.add({self.city['_id']: rec01_html})
            rec01_css = Recommendation01(self.sourcecode, url=self.city['url']).validar_css()
            self.occurrences.add({self.city['_id']: rec01_css})
            rec00_cms = Recommendation00(self.city['url']).identify()
            self.occurrences.add({self.city['_id']: rec00_cms})

    def get_occurrences(self):
        return self.occurrences.convert()
