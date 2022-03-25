#Email Modules
from email.mime.text import MIMEText

#Django
from django.utils.encoding import smart_str
from django.template import Template, Context

#Local Modules
import smtplib
import os
from os import getenv as venv

class MailType:
    HTML = 'html'
    TEXT = 'text

class Carmeil:
    def __init__(self, from_, to, subject, template_name **kwargs):
        """
        params
        from
        to
        subject
        template_name
        --opt
        type
        header
        sign
        """
        self.from_ = kwargs['from']
        self.to = kwargs['to']
        self.subject = kwargs['subject']
        self.template_name = template_name

        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()

        self.format = MailType.TEXT
        if(kwargs.has_key('type')):
            self.format = kwargs['type']

        if self.format == MailType.HTML:
            file_name = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                template_name
                )
            template_file = open(file_name, "r")
            self.template = Template(template_file.read())
            template_file.close()


        if(kwargs.has_key('header'):
            self.cabecera = kwargs['header']
        if(kwargs.has_key('template_name'):
            self.firma = kwargs['sign']

    def server_login(self):
        self.server.login(
                venv('EMAIL_USER'),
                venv('EMAIL_PASSWORD')
                )

    def send(self, login):
        self.server_login()
        if self.format == MailType.TEXT:
            #leer mensaje de algun template con f strings
            # msg = template(args)
            pass
        elif self.format == MailType.HTML:
            context = Context({#aqui colocas el context dependiendo del template
                "field 1": "value1",
                "field 2": "value2",
                }
                )
            html_render = smart_str(self.template.render(context, encoding='utf-8'))
            msg = MIMEText(html_render, 'html')

        msg['Subject'] = self.subject
        self.server.sendmail(
                self.from_,
                self.to,
                msg.as_string()
                )
        print('reservas insuficientes: Email sent')
