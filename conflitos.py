import datetime 
from Compromisso import Compromisso

class Conflitos:
    def verificar_conflito(comp1: Compromisso, comp2: Compromisso):
        if not comp1.datahora or not comp2.datahora:
            return False
        
        fim_comp1 = comp1.datahora + datetime.timedelta(minutes=comp1.getduracao())
        fim_comp2 = comp2.datahora + datetime.timedelta(minutes=comp2.getduracao())

        conflito = (comp1.datahora < fim_comp2) and (comp2.datahora < fim_comp1)

        return conflito