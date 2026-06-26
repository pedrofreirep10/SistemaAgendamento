from datetime import datetime, timedelta, date

class Appointment:
    """
    Representa um compromisso individual. 
    Criada aqui para demonstrar o relacionamento com a Schedule.
    """
    def __init__(self, title: str, start_time: datetime, duration_minutes: int, description: str = ""):
        self._title = title
        self._start_time = start_time
        self._duration = timedelta(minutes=duration_minutes)
        self._description = description

    @property
    def title(self) -> str:
        return self._title

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @property
    def end_time(self) -> datetime:
        # O horário de término é calculado dinamicamente
        return self._start_time + self._duration

    def __str__(self) -> str:
        return f"[{self.start_time.strftime('%d/%m/%Y %H:%M')} - {self.end_time.strftime('%H:%M')}] {self.title}"


class Schedule:
    """
    Orquestra e gerencia a coleção de compromissos, aplicando as regras de negócio
    como ordenação, filtros temporais e detecção de conflitos de horário.
    """
    def __init__(self):
        # Encapsulamento: a lista de compromissos é privada para evitar manipulação externa direta
        self._appointments: list[Appointment] = []

    def has_conflict(self, new_appointment: Appointment) -> bool:
        """
        Verifica se o novo compromisso se sobrepõe a algum compromisso já agendado.
        Lógica matemática de intervalos: Dois eventos [A, B] e [C, D] se sobrepõem se (A < D) e (C < B).
        """
        for existing_app in self._appointments:
            if new_appointment.start_time < existing_app.end_time and existing_app.start_time < new_appointment.end_time:
                return True
        return False

    def add_appointment(self, appointment: Appointment) -> bool:
        """
        Adiciona um compromisso à agenda caso não haja conflito de horário.
        Mantém a lista sempre ordenada por horário de início.
        """
        if self.has_conflict(appointment):
            raise ValueError(f"Alerta de conflito: O horário para '{appointment.title}' já está ocupado.")
        
        self._appointments.append(appointment)
        # Ordena automaticamente por horário de início para facilitar as visualizações
        self._appointments.sort(key=lambda app: app.start_time)
        return True

    def remove_appointment(self, title: str) -> bool:
        """
        Busca e remove um compromisso pelo título (case-insensitive).
        Retorna True se removido com sucesso, False caso contrário.
        """
        for appointment in self._appointments:
            if appointment.title.lower() == title.lower():
                self._appointments.remove(appointment)
                return True
        return False

    def get_appointments_by_day(self, target_date: date) -> list[Appointment]:
        """
        Filtra e retorna os compromissos de um dia específico.
        """
        return [app for app in self._appointments if app.start_time.date() == target_date]

    def get_appointments_by_week(self, start_date: date) -> list[Appointment]:
        """
        Filtra e retorna os compromissos dentro do intervalo de uma semana (7 dias)
        a partir de uma data inicial.
        """
        end_date = start_date + timedelta(days=7)
        return [app for app in self._appointments if start_date <= app.start_time.date() < end_date]

    def __str__(self) -> str:
        """Retorna uma representação legível em formato de texto de toda a agenda."""
        if not self._appointments:
            return "Nenhum compromisso agendado."
        return "\n".join(str(app) for app in self._appointments)

    def __repr__(self) -> str:
        """Retorna a assinatura técnica do estado atual do objeto."""
        return f"Schedule(total_appointments={len(self._appointments)})"