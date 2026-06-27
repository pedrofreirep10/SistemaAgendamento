import datetime

class Compromisso:
    def __init__(self, id, nome, descricao, data, hora, duracao):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        try:
            self.duracao = int(duracao)
        except (ValueError, TypeError):
            print(f"Aviso: duração inválida '{duracao}', definida como 0.")
            self.duracao = 0

        string_datahora = f"{data} {hora}"
        try:
            self.datahora = datetime.datetime.strptime(string_datahora, "%d/%m/%Y %H:%M")
        except ValueError:
            print(f"Erro ao criar compromisso '{nome}': Formato inválido. Use DD/MM/AAAA HH:MM.")
            self.datahora = None

    def getdata(self):
        if self.datahora:
            return self.datahora.date()
        return None

    def gethora(self):
        if self.datahora:
            return self.datahora.time()
        return None

    def getdatahora(self):
        return self.datahora

    def getnome(self):
        return self.nome

    def getdescricao(self):
        return self.descricao

    def getid(self):
        return self.id

    def getduracao(self):
        return self.duracao

    def setnome(self, nome):
        self.nome = nome

    def setdatahora(self, data, hora):
        string_datahora = f"{data} {hora}"
        try:
            self.datahora = datetime.datetime.strptime(string_datahora, "%d/%m/%Y %H:%M")
        except ValueError:
            print("Erro: Formato de data/hora inválido. As alterações não foram salvas. Use DD/MM/AAAA HH:MM.")

    def setdescricao(self, descricao):
        self.descricao = descricao

    def setduracao(self, duracao):
        try:
            self.duracao = int(duracao)
        except (ValueError, TypeError):
            print(f"Aviso: duração inválida '{duracao}', valor não alterado.")

    def __str__(self):
        if self.datahora:
            data_formatada = self.datahora.date()
            hora_formatada = self.datahora.time()
        else:
            data_formatada = "Inválida"
            hora_formatada = "Inválida"
        return (f"\tCompromisso: \n| Id:{self.id}\n"
                f"Nome: {self.nome}\n"
                f"Descrição: {self.descricao}\n"
                f"Data: {data_formatada}\n"
                f"Hora: {hora_formatada}\n"
                f"Duração: {self.duracao} min\n")