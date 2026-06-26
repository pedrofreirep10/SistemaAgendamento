import datetime
class Compromisso:
    def __init__(self, id, nome, descricao, data, hora, duracao):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.duracao = duracao
        string_datahora = f"{data} {hora}"
        try:
            self.datahora = datetime.datetime.strptime(string_datahora, "%d/%m/%Y %H:%M")
        except ValueError:
            #se der erro de valor/formato, avisa o usuário e define como None (nulo)
            print(f"Erro ao criar compromisso '{nome}': Formato inválido. Use DD/MM/AAAA HH:MM.")
            self.datahora = None

    #get para data do compromisso
    def getdata(self):
        if self.datahora:
            return self.datahora.date()
        return "Data não definida" #se for None

    #get para hora do compromisso
    def gethora(self):
        if self.datahora:
            return self.datahora.time()
        return "Hora não definida" #se for None

    #get para nome do compromisso
    def getnome(self):
        return self.nome

    #get para descrição do compromisso
    def getdescricao(self):
        return self.descricao

    #get para o id do compromisso
    def getid(self):
        return self.id
    
    #get para a duracao do compromisso
    def getduracao(self):
        return self.duracao

    #set para nome do compromisso
    def setnome(self,nome):
        self.nome = nome

    # set para data e hora
    def setdatahora(self, data, hora):
        string_datahora = f"{data} {hora}"
        try:
            self.datahora = datetime.datetime.strptime(string_datahora, "%d/%m/%Y %H:%M")
        except ValueError:
            print("Erro: Formato de data/hora inválido. As alterações não foram salvas. Use DD/MM/AAAA HH:MM.")

    #set para descrição
    def setdescricao(self,descricao):
        self.descricao = descricao

    def __str__(self):
        if self.datahora:
            data_formatada = self.datahora.date()
            hora_formatada = self.datahora.time()
        else:
            data_formatada = "Inválida"
            hora_formatada = "Inválida"

        return f"Compromisso: Id:{self.id} | Nome:{self.nome} | Descrição:{self.descricao} | Data:{data_formatada} | Hora:{hora_formatada}"