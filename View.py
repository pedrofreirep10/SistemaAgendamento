import datetime
from Compromisso import Compromisso

class CalendarView:
    def __init__(self, lista_de_compromissos):
        self.agenda = lista_de_compromissos

    def mostrar_dia(self, data_texto: str):
        try:
            data_alvo = datetime.datetime.strptime(data_texto, "%d/%m/%Y").date()
        except ValueError:
            print("\nErro: Formato de data inválido. Use DD/MM/AAAA.")
            return

        print(f"\n| Agenda do Dia: {data_texto}\n")
        encontrou_compromisso = False

        compromissos_do_dia = sorted(
            [comp for comp in self.agenda if comp.getdata() == data_alvo],
            key=lambda c: c.gethora()
        )

        for comp in compromissos_do_dia:
            hora = comp.gethora()
            hora_str = hora.strftime("%H:%M") if isinstance(hora, datetime.time) else "??:??"
            print(f"{hora_str}\t- {comp.getnome()} (Duração: {comp.getduracao()} min)")

            if comp.getdescricao():
                print(f"\tDetalhes: {comp.getdescricao()}\n")

            encontrou_compromisso = True

        if not encontrou_compromisso:
            print("Nenhum compromisso agendado para este dia.")
        print("-" * 50)

    def mostrar_semana(self, data_inicial_texto: str):
        try:
            data_inicial = datetime.datetime.strptime(data_inicial_texto, "%d/%m/%Y").date()
        except ValueError:
            print("Erro: Formato de data inválido. Use DD/MM/AAAA.")
            return

        print(f"\n| Agenda da Semana a partir de {data_inicial_texto}\n")

        for i in range(7):
            dia_atual = data_inicial + datetime.timedelta(days=i)
            dia_atual_texto = dia_atual.strftime("%d/%m/%Y")
            self.mostrar_dia(dia_atual_texto)
