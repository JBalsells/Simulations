"""
Sobrecarga — Ejemplo 7: Notificaciones
=======================================
Sobrecarga de método propio mediante herencia: enviar()

  Notificacion          → define enviar() base (solo registra)
  NotificacionEmail     → sobrecarga enviar() agregando envío por email
  NotificacionSMS       → sobrecarga enviar() agregando envío por SMS
"""


class Notificacion:
    def enviar(self, mensaje: str):
        print(f"[LOG] {mensaje}")


class NotificacionEmail(Notificacion):
    def __init__(self, destinatario: str):
        self.destinatario = destinatario

    def enviar(self, mensaje: str):
        super().enviar(mensaje)
        print(f"[EMAIL → {self.destinatario}] {mensaje}")


class NotificacionSMS(Notificacion):
    def __init__(self, telefono: str):
        self.telefono = telefono

    def enviar(self, mensaje: str):
        super().enviar(mensaje)
        print(f"[SMS → {self.telefono}] {mensaje[:20]}...")


if __name__ == "__main__":
    base  = Notificacion()
    email = NotificacionEmail("user@mail.com")
    sms   = NotificacionSMS("+1-555-0100")

    print("--- Notificacion base ---")
    base.enviar("Sistema iniciado")

    print("\n--- Email ---")
    email.enviar("Tu pedido fue enviado")

    print("\n--- SMS ---")
    sms.enviar("Tu pedido fue enviado")
