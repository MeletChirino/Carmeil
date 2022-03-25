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
        context
        header
        sign
        CC
        CCo
        """
        self.from_ = kwargs['from']
        self.to = kwargs['to']
        self.subject = kwargs['subject']
        self.template_name = template_name

        self.server = smtplib.SMTP(
                'smtp.gmail.com',
                587
                )
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()

        self.format = MailType.TEXT
        if(kwargs.has_key('type')):
            self.format = kwargs['type']

        self.CC = ''
        if(kwargs.has_key('CC')):
            self.format = kwargs['CC']

        self.CCo = ''
        if(kwargs.has_key('CCo')):
            self.format = kwargs['CCo']

        if self.format == MailType.HTML:
            file_name = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                template_name
                )
            template_file = open(file_name, "r")
            self.template = Template(template_file.read())
            template_file.close()
            self.context = kwargs['context']


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
            context = Context(self.context)
            html_render = smart_str(
                self.template.render(
                    context,
                    encoding='utf-8'
                    )
                )
            msg = MIMEText(html_render, 'html')

        msg['Subject'] = self.subject
        self.server.sendmail(
                self.from_,
                self.to,
                msg.as_string()
                )
        if (self.save == False):
            Message(
                sender = self.from_,
                receiver = self.to,
                CC = self.CC,
                CCo = self.CCo,
                body = self.msg['body'],
                format = self.format
                )
        print('Email sent')
