import json
import os

class Armazenamento:
    def __init__(self, nome_arquivo = 'agenda.json'):
        self.nome_arquivo = nome_arquivo

        if not os.path.exists(self.nome_arquivo):
            with open(self.nome_arquivo, "w") as arquivo:
                json.dump([], arquivo)

    def carregar_compromisso(self):
        with open(self.nome_arquivo, "r") as arquivo:
            dados = json.load(arquivo)
            return dados
    
    def salvar_compromisso(self, lista_compromisso):
        with open(self.nome_arquivo , "w") as arquivo:
            json.dump(lista_compromisso, arquivo, indent=4)
