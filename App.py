import datetime
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
        self.carregar_dados()
        self.visao = CalendarView(self.compromissos)

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
            datahora = compromisso.getdatahora()
            hora_obj = compromisso.gethora()
            dados.append({
                "id": compromisso.getid(),
                "nome": compromisso.getnome(),
                "descricao": compromisso.getdescricao(),
                "data": datahora.strftime("%d/%m/%Y") if datahora else "",
                "hora": hora_obj.strftime("%H:%M") if hora_obj else "",
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
                from datetime import timedelta
                fim_atual = compromisso.datahora + timedelta(minutes=compromisso.getduracao())
                fim_novo = novo_compromisso.datahora + timedelta(minutes=novo_compromisso.getduracao())
                if compromisso.datahora < fim_novo and novo_compromisso.datahora < fim_atual:
                    return True
        return False

    def cadastrar_compromisso(self):
        print("\n| Cadastrar Compromisso")
        nome = input("Nome: ").strip()
        descricao = input("Descrição: ").strip()
        data = input("Data (DD/MM/AAAA): ").strip()
        hora = input("Hora (HH:MM): ").strip()
        while True:
            duracao_texto = input("Duração em minutos: ").strip()
            try:
                duracao = int(duracao_texto)
                break
            except ValueError:
                print("Duração inválida. Digite um número inteiro.")

        novo_id = self.gerar_proximo_id()
        compromisso = Compromisso(novo_id, nome, descricao, data, hora, duracao)

        if compromisso.datahora is None:
            print("Compromisso não cadastrado por erro de data/hora.")
            return

        if self.verificar_conflito(compromisso):
            print("Conflito de horário detectado! Compromisso não cadastrado.")
            return

        self.compromissos.append(compromisso)
        self.salvar_dados()
        print(f"Compromisso '{nome}' cadastrado com sucesso! (ID: {novo_id})")

    def listar_compromissos(self):
        print("\n| Lista de Compromissos")
        if not self.compromissos:
            print("Nenhum compromisso cadastrado.")
            return
        for comp in sorted(self.compromissos, key=lambda c: c.datahora):
            print(comp)

    def editar_compromisso(self):
        print("\n| Editar Compromisso ")
        self.listar_compromissos()
        try:
            id_alvo = int(input("Digite o ID do compromisso a editar: ").strip())
        except ValueError:
            print("ID inválido.")
            return

        alvo = next((c for c in self.compromissos if c.getid() == id_alvo), None)
        if alvo is None:
            print("Compromisso não encontrado.")
            return

        print("Deixe em branco para manter o valor atual.")
        nome = input(f"Nome [{alvo.getnome()}]: ").strip()
        descricao = input(f"Descrição [{alvo.getdescricao()}]: ").strip()
        data_input = input(f"Data [{alvo.getdatahora().strftime('%d/%m/%Y')}]: ").strip()
        hora_input = input(f"Hora [{alvo.getdatahora().strftime('%H:%M')}]: ").strip()
        duracao_input = input(f"Duração em minutos [{alvo.getduracao()}]: ").strip()

        if nome:
            alvo.setnome(nome)
        if descricao:
            alvo.setdescricao(descricao)
        if data_input or hora_input:
            data_final = data_input or alvo.getdatahora().strftime("%d/%m/%Y")
            hora_final = hora_input or alvo.getdatahora().strftime("%H:%M")
            alvo.setdatahora(data_final, hora_final)
        if duracao_input:
            alvo.setduracao(duracao_input)

        self.salvar_dados()
        print("Compromisso atualizado com sucesso!")

    def excluir_compromisso(self):
        print("\n| Excluir Compromisso")
        self.listar_compromissos()
        try:
            id_alvo = int(input("Digite o ID do compromisso a excluir: ").strip())
        except ValueError:
            print("ID inválido.")
            return

        alvo = next((c for c in self.compromissos if c.getid() == id_alvo), None)
        if alvo is None:
            print("Compromisso não encontrado.")
            return

        self.compromissos.remove(alvo)
        self.salvar_dados()
        print(f"Compromisso ID {id_alvo} excluído com sucesso!")

    def visualizar_dia(self):
        print("\n| Agenda do Dia")
        data_texto = input("Digite a data (DD/MM/AAAA): ").strip()
        self.visao.mostrar_dia(data_texto)

    def visualizar_semana(self):
        print("\n| Agenda da Semana ")
        data_texto = input("Digite a data inicial da semana (DD/MM/AAAA): ").strip()
        self.visao.mostrar_semana(data_texto)

    def run(self):
        opcoes = {
            "1": ("Cadastrar compromisso", self.cadastrar_compromisso),
            "2": ("Listar todos os compromissos", self.listar_compromissos),
            "3": ("Editar compromisso", self.editar_compromisso),
            "4": ("Excluir compromisso", self.excluir_compromisso),
            "5": ("Visualizar agenda do dia", self.visualizar_dia),
            "6": ("Visualizar agenda da semana", self.visualizar_semana),
            "0": ("Sair", None),
        }

        while True:
            print("\n| Menu\n")
            for chave, (descricao, _) in opcoes.items():
                print(f"  [{chave}] {descricao}")

            escolha = input("\nEscolha uma opção: ").strip()

            if escolha == "0":
                print("Encerrando. Até logo!")
                break
            elif escolha in opcoes:
                _, acao = opcoes[escolha]
                acao()
            else:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    App().run()
