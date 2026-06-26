from datetime import datetime, timedelta

from Compromisso import Compromisso
from Armazenamento import Armazenamento

try:
    from conflitos import Conflitos
except ImportError:
    Conflitos = None

class App:
    def __init__(self):
        self.armazenamento = Armazenamento()
        self.compromisso = []
        self.carregar_dados

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
                    self.compromisso.append(compromisso)

            except KeyError:
                print("Erro ao carregar um compromisso: dados incompletos no arquivo JSON.")

    def salvar_dados(self):
        dados = []

        for compromisso in self.compromisso:
            dados.append({
                "id": compromisso.getid(),
                "nome": compromisso.getnome(),
                "descricao": compromisso.getdescricao(),
                "data": compromisso.getdatahora.strftime("%d/%m/%Y"),
                "hora": compromisso.gethora.strftime("%H:%M"),
                "duracao": compromisso.getduracao(),
            })

        self.armazenamento.salvar_compromisso(dados)

    def gerar_proximo_id(self):
        if not self.compromisso:
            return 1

        maior_id = max(compromisso.getid() for compromisso in self.compromisso)
        return maior_id + 1

    def verificar_conflito(self, novo_compromisso):
        for compromisso in self.compromissos:
            if Conflitos is not None:
                if Conflitos.verificar_conflito(compromisso, novo_compromisso):
                    return True
            else:
                fim_atual = compromisso.datahora + timedelta(minutes=compromisso.getduracao())
                fim_novo = novo_compromisso.datahora + timedelta(minutes=novo_compromisso.getduracao())

                if compromisso.datahora < fim_novo and novo_compromisso.datahora < fim_atual:
                    return True

        return False

    def cadastrar_compromisso(self):
        print("\n=== Cadastrar compromisso ===")

        nome = input("Nome: ").strip()
        descricao = input("Descrição: ").strip()
        data = input("Data (DD/MM/AAAA): ").strip()
        hora = input("Hora (HH:MM): ").strip()

        try:
            duracao = int(input("Duração em minutos: ").strip())
        except ValueError:
            print("Erro: duração precisa ser um número inteiro.")
            return

        if duracao <= 0:
            print("Erro: duração precisa ser maior que zero.")
            return

        novo = Compromisso(
            self.gerar_proximo_id(),
            nome,
            descricao,
            data,
            hora,
            duracao
        )

        if novo.datahora is None:
            print("Compromisso não cadastrado por erro de data ou hora.")
            return

        if self.verificar_conflito(novo):
            print("Alerta: existe conflito de horário com outro compromisso.")
            return

        self.compromissos.append(novo)
        self.compromissos.sort(key=lambda compromisso: compromisso.datahora)
        self.salvar_dados()

        print("Compromisso cadastrado com sucesso.")

    def listar_compromissos(self):
        print("\n=== Lista de compromissos ===")

        if not self.compromissos:
            print("Nenhum compromisso cadastrado.")
            return

        for compromisso in sorted(self.compromissos, key=lambda c: c.datahora):
            print(compromisso)

    def remover_compromisso(self):
        print("\n=== Remover compromisso ===")

        try:
            id_remover = int(input("Digite o ID do compromisso: ").strip())
        except ValueError:
            print("Erro: ID inválido.")
            return

        for compromisso in self.compromissos:
            if compromisso.getid() == id_remover:
                self.compromissos.remove(compromisso)
                self.salvar_dados()
                print("Compromisso removido com sucesso.")
                return

        print("Compromisso não encontrado.")

    def visualizar_dia(self):
        print("\n=== Agenda do dia ===")

        data_texto = input("Digite a data (DD/MM/AAAA): ").strip()

        try:
            data_alvo = datetime.strptime(data_texto, "%d/%m/%Y").date()
        except ValueError:
            print("Erro: data inválida. Use DD/MM/AAAA.")
            return

        compromissos_dia = [
            compromisso for compromisso in self.compromissos
            if compromisso.datahora.date() == data_alvo
        ]

        if not compromissos_dia:
            print("Nenhum compromisso nesse dia.")
            return

        # TODO: substituir isso pela classe CalendarView quando ela ficar pronta.
        for compromisso in sorted(compromissos_dia, key=lambda c: c.datahora):
            print(compromisso)

    def visualizar_semana(self):
        print("\n=== Agenda da semana ===")

        data_texto = input("Digite a data inicial da semana (DD/MM/AAAA): ").strip()

        try:
            inicio = datetime.strptime(data_texto, "%d/%m/%Y").date()
        except ValueError:
            print("Erro: data inválida. Use DD/MM/AAAA.")
            return

        fim = inicio + timedelta(days=7)

        compromissos_semana = [
            compromisso for compromisso in self.compromissos
            if inicio <= compromisso.datahora.date() < fim
        ]

        if not compromissos_semana:
            print("Nenhum compromisso nessa semana.")
            return

        # TODO: substituir isso pela classe CalendarView quando ela ficar pronta.
        for compromisso in sorted(compromissos_semana, key=lambda c: c.datahora):
            print(compromisso)

    def exibir_menu(self):
        print("\n===== Sistema de Agendamento =====")
        print("1 - Cadastrar compromisso")
        print("2 - Listar compromissos")
        print("3 - Remover compromisso")
        print("4 - Visualizar agenda do dia")
        print("5 - Visualizar agenda da semana")
        print("0 - Sair")

    def executar(self):
        while True:
            self.exibir_menu()
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.cadastrar_compromisso()
            elif opcao == "2":
                self.listar_compromissos()
            elif opcao == "3":
                self.remover_compromisso()
            elif opcao == "4":
                self.visualizar_dia()
            elif opcao == "5":
                self.visualizar_semana()
            elif opcao == "0":
                self.salvar_dados()
                print("Sistema encerrado.")
                break
            else:
                print("Opção inválida.")

if __name__ == "__main__":
    app = App()
    app.executar()



