#Email Modules
from email.mime.text import MIMEText
from email.message import EmailMessage

#Django
from django.utils.encoding import smart_str
from django.template import Template, Context

#Local Modules
import smtplib
import os
from os import getenv as venv
from .templates import sign, message

class MailType:
    HTML = 'html'
    TEXT = 'text'

class Carmeil:
    def __init__(self, from_, to, subject, template_name, **kwargs):
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
        self.from_ = from_
        self.to = to
        self.subject = subject
        self.template_name = template_name

        self.server = smtplib.SMTP(
                'smtp.gmail.com',
                587
                )
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()

        self.format = MailType.TEXT
        if(kwargs.get('type')):
            self.format = kwargs['type']

        if(kwargs.get('content')):
            self.content = kwargs['content']

        self.CC = ''
        if(kwargs.get('CC')):
            self.format = kwargs['CC']

        self.CCo = ''
        if(kwargs.get('CCo')):
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


        if(kwargs.get('header')):
            self.cabecera = kwargs['header']
        if(kwargs.get('sign')):
            self.firma = kwargs['sign']

    def server_login(self):
        self.server.login(
                venv('EMAIL_USER'),
                venv('EMAIL_PASSWORD')
                )

    def send(self):
        self.server_login()
        if self.format == MailType.TEXT:
            #leer mensaje de algun template con f strings
            # msg = template(args)
            msg = EmailMessage()
            msg.set_content(self.content)
            msg['Subject'] = self.subject
            msg["From"] = self.from_
            msg['To'] = self.to
            self.server.send_message(msg)
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
        '''
        if (self.save == False):
            Message(
                sender = self.from_,
                receiver = self.to,
                CC = self.CC,
                CCo = self.CCo,
                body = self.msg['body'],
                format = self.format
                )
        #you should save all this
        '''
        print('Email sent')
