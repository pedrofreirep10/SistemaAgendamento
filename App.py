from datetime import datetime, timedelta
from View import CalendarView
from Compromisso import Compromisso
from Armazenamento import Armazenamento

try:
    from conflitos import Conflitos
except ImportError:
    Conflitos = None

class App:
    def __init__(self):
        self.armazenamento = Armazenamento()
        self.compromissos = [] 
        
        self.visao = CalendarView(self.compromissos) 
        
        self.carregar_dados()

    def carregar_dados(self):
        dados = self.armazenamento.carregar_compromisso()
        for item in dados:
            try:
                compromisso = Compromisso(
                    item["id"],
                    item["nome"],
                    item["descricao"],
                    item["data"],
                    item["hora"],
                    item["duracao"],
                )
                if compromisso.datahora is not None:
                    self.compromissos.append(compromisso)
            except KeyError:
                print("Erro ao carregar um compromisso: dados incompletos no arquivo JSON.")

    def salvar_dados(self):
        dados = []
        for compromisso in self.compromissos:
            dados.append({
                "id": compromisso.getid(),
                "nome": compromisso.getnome(),
                "descricao": compromisso.getdescricao(),
                "data": compromisso.getdatahora().strftime("%d/%m/%Y") if compromisso.getdatahora() else "",
                "hora": compromisso.gethora().strftime("%H:%M") if compromisso.gethora() else "",
                "duracao": compromisso.getduracao(),
            })
        self.armazenamento.salvar_compromisso(dados)

    def gerar_proximo_id(self):
        if not self.compromissos: 
            return 1
        maior_id = max(c.getid() for c in self.compromissos)
        return maior_id + 1

    def verificar_conflito(self, novo_compromisso):
        for compromisso in self.compromissos:
            if Conflitos is not None:
                if Conflitos.verificar_conflito(compromisso, novo_compromisso):
                    return True
            else:
                fim_atual = compromisso.datahora + timedelta(minutes=int(compromisso.getduracao().split()[0]) if isinstance(compromisso.getduracao(), str) else compromisso.getduracao())
                fim_novo = novo_compromisso.datahora + timedelta(minutes=int(novo_compromisso.getduracao().split()[0]) if isinstance(novo_compromisso.getduracao(), str) else novo_compromisso.getduracao())

                if compromisso.datahora < fim_novo and novo_compromisso.datahora < fim_atual:
                    return True
        return False


    def visualizar_dia(self):
        print("\n=== Agenda do dia ===")
        data_texto = input("Digite a data (DD/MM/AAAA): ").strip()
        
        self.visao.mostrar_dia(data_texto)

    def visualizar_semana(self):
        print("\n=== Agenda da semana ===")
        data_texto = input("Digite a data inicial da semana (DD/MM/AAAA): ").strip()
        
        self.visao.mostrar_semana(data_texto)
