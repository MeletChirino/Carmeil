#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Email Modules
from email.mime.text import MIMEText

#Django
from django.utils.encoding import smart_str
from django.template import Template, Context

#Local Modules
import smtplib
import os
import json

with open('/etc/config.json') as config_file:
    config = json.load(config_file)


class NotificacionReserva:
    def __init__(self, email_info):
        self.email_data = email_info
        #ATENCCION!! EN MASTER CAMBIA ESTA VAINA POR EL DOMINIO QUE ES
        self.web_domain = "http://localhost:8000"
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()

        self.server.login(config['EMAIL_USER'],
                config['EMAIL_PASSWORD'])

        #self.msg = f'Subject: {subject}\n\n{body}'
        file_name = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "mail_template.html"
            )
        template_file = open(file_name, "r")
        self.template = Template(template_file.read())
        template_file.close()
        self.cabecera = "Estimad@ " + str(self.email_data['nombre']) + "\n\n"
        self.firma = ("\n\nCon amor, \n\n"
                "Equipo de Reservas\nHotel Casa Andrea\n"
                "Cra 3 No. 5 - 76\n"
                "Cel: 300 610 1753 - 312 622 6069"
                )

    def reservas_insuficientes(self):
        '''
        Este correo se envia como notificacion no hay dispponibilidad en las habitaciones
        '''
        text = ("Alguien solicito una resreva para el dia"
                " %s y no hay disponibilidad para la fecha, deberias "
                "agregar habitaciones para %s personas para"
                " esos dias") % ( self.email_data['fecha'].strftime("%d %B %Y"),
                        self.email_data['pax']
                            )
        context = Context({
            "header": "Reservas Insuficientes",
            "msg": text,
            "domain": self.web_domain,
            })
        html_render = smart_str(self.template.render(context), encoding='utf-8')
        msg = MIMEText(html_render, 'html')
        msg['Subject'] = 'Reservas insuficientes'
        sender_mail = "Equipo de Reservas"
        receiver_mail = 'melet.chirino@gmail.com'
        self.server.sendmail(
                sender_mail,
                receiver_mail,
                msg.as_string()
                )
        print('reservas insuficientes: Email sent')

    def recibo_invalido(self):
        #si la reserva fue aceptada vas a enviar esto
        text = ("Te informamos que nuestro equipo de reservas"
                "encontro que tu recibo es invalido o la foto"
                "no se observa bien. Te invitamos a subir otra "
                "vez la foto de tu comprobante para confirmar tu "
                "reserva llo antes posible. Puedes subir tu fot en "
                "el siguiente link " +
                self.web_domain + "/pago/" +
                str(self.email_data['id_reserva']) +
                ". Estamos para servirte"
                )
        context = Context({
            "header": "Recibo Invalido",
            "msg": text,
            "link": self.email_data['id_reserva'],
            "domain": self.web_domain,
            })
        html_render = smart_str(self.template.render(context), encoding='utf-8')
        msg = MIMEText(html_render, 'html')
        msg['Subject'] = "Recibo Invalido"
        msg["From"] = "Equipo de Reservas"
        msg['To'] =  self.email_data['correo']
        sender_mail = "Equipo de Reservas"
        receiver_mail = self.email_data['correo']
        self.server.sendmail(
                sender_mail,
                receiver_mail,
                msg.as_string()
                )
        print('recibo_invalido: Email sent')

    def aceptada(self):
        #si la reserva fue aceptada va a enviar esto
        text =("Te informamos que tenemos disponibilidad para "
                "tu reserva del día " +
                str(self.email_data['check_in']) +
                ". Las reservas sin anticipo se guardan hasta "
                "las 12m del día de la reserva. \n\nPara confirmar "
                "tu reserva se requiere el pago de la primera "
                "noche de estadía en la cuenta de ahorros "
                "Bancolombia de No. 78932017597. Si realiza "
                "consignacion nacional debe cancelar adicionalmente "
                " $13.000 (TRECE MIL PESOS) por concepto de costo de "
                "la transaccion. Las transferencias entre cuentas "
                "Bancolombia no tienen ningun costo. Una vez realizado "
                " el pago por favor ingresarlo en la siguiente página "
                + self.web_domain + "/pago/" +
                str(self.email_data['id_reserva']) +
                ", puedes tomarle una foto con tu celular y montarlo "
                "en ese link.\nEsperamos saber pronto de ti."
                )

        context = Context({
            "header": "Reserva Aceptada",
            "msg": text,
            "link": self.email_data['id_reserva'],
            "domain": self.web_domain,
            })
        html_render = smart_str(self.template.render(context), encoding='utf-8')
        msg = MIMEText(html_render, 'html')
        msg['Subject'] = 'Reserva Aceptada'
        msg["From"] = "Equipo de Reservas"
        msg['To'] =  self.email_data['correo']
        sender_mail = "Equipo de Reservas"
        receiver_mail = self.email_data['correo']
        self.server.sendmail(
                sender_mail,
                receiver_mail,
                msg.as_string()
                )
        print('aceptada : Email sent')

    def confirmada(self):
        #si la reserva es confirmada se enviará el email por aqui
        check_in = self.email_data['check_in'].strftime("%d %B %Y")
        check_out = self.email_data['check_out'].strftime("%d %B %Y")
        text = ("Con este mensaje confirmamos tu "
                "reserva en nuestro hotel.\nTe "
                "adjuntamos los detalles de la misma:\n"
                "- Nombre: %s\n"
                "- Personas: %s\n"
                "- Fecha de entrada: %s\n"
                "- Fecha de salida: %s\n"
                "Esta reserva será válida hasta "
                "medio día del dia de la reserva."
                "Por favor ingresa en el siguiente "
                "link para validar tu reserva: "
                ) % (self.email_data['nombre'],
                        self.email_data['personas'],
                        check_in,
                        check_out
                        )
        text2 = (" Si tienes algun tipo de retraso por "
                "favor comunicate con nosotros."
                "Te esperamos pronto")

        context = Context({
            "header": "Reserva Confirmada",
            "msg": text,
            "msg2": text2,
            "link": self.email_data['id_reserva'],
            "domain": self.web_domain,
            })
        html_render = smart_str(self.template.render(context), encoding='utf-8')
        msg = MIMEText(html_render, 'html')
        msg['Subject'] = 'Reserva Confirmada'
        msg["From"] = "Equipo de Reservas"
        msg['To'] =  self.email_data['correo']
        sender_mail = "Equipo de Reservas"
        receiver_mail = self.email_data['correo']
        self.server.sendmail(
                sender_mail,
                receiver_mail,
                msg.as_string()
                )
        print('confirmada: Email sent')

    def cancelada(self):
        #si la reserva es cancelada se enviará el email por aqui
        text = ("Lamentamos informarte que no tenemos "
                "disponibilidad de habitaciones para tu "
                "reserva del dia " +
                str(self.email_data['check_in']) +
                " . Deseabamos ser el anfitrión de tu "
                "estadía en Cartagena. Esperamos saber "
                "de ti pronto para otro día que te animes "
                "a visitar Cartagena con nosotros."
                )

        context = Context({
            "header": "Reserva Cancelada",
            "msg": text,
            })
        html_render = smart_str(self.template.render(context), encoding='utf-8')
        msg = MIMEText(html_render, 'html')
        msg['Subject'] = 'Reserva Cancelada'
        msg["From"] = "Equipo de Reservas"
        msg['To'] =  self.email_data['correo']
        sender_mail = "Equipo de Reservas"
        receiver_mail = self.email_data['correo']
        self.server.sendmail(
                sender_mail,
                receiver_mail,
                msg.as_string()
                )
        print('cancelada : Email sent')

    def pagada(self):
        #este mensaje se envia automaticamente cuando una reserva es guardada en el sistema

        text = ("Nuestro equipo de reservas ha verificado "
                "el pago de tu reserva el dia " +
                str(self.email_data['check_in']) +
                " al día " + str(self.email_data["check_out"]) +
                " para " + str(self.email_data['personas']) +
                " personas. Te esperamos."
                )

        context = Context({
            "header": "Reserva Confirmada",
            "msg": text,
            "link": self.email_data['id_reserva'],
            "domain": self.web_domain,
            })
        html_render = smart_str(self.template.render(context), encoding='utf-8')
        msg = MIMEText(html_render, 'html')
        msg['Subject'] = 'Reserva Confirmada'
        msg["From"] = "Equipo de Reservas"
        msg['To'] =  self.email_data['correo']
        sender_mail = "Equipo de Reservas"
        receiver_mail = self.email_data['correo']
        self.server.sendmail(
                sender_mail,
                receiver_mail,
                msg.as_string()
                )
        print('pagada : Email sent')
