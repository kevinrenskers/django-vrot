"""--------------------------------------------------------------------------------
Copyright (c) 2011, Kevin Renskers and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of django-vrot nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
-----------------------------------------------------------------------------------

Generic email system for Django

- It will send text email if there is a custom text template,
  or when using default template, when text_body is set
- It will send html email if there is a custom html template,
  or when using default template, when html_body is set
- You can also force to send a text email when there is only a html_body,
  it will then convert html to text
- You can also force to send a html email when there is only a text_body,
  it will then convert text to html


USAGE

from vrot.generic_email import Email

# This will send text email only, uses the email/base_text_email.html template with the "body" template variable
email = Email('to@example.com', 'Subject', 'Line one\n\nLine two')
email.send()

# This will send text- and html email, also with default template
email = Email('to@example.com', 'Subject', 'Line one\n\nLine two', '<p>Line one</p><p>Line two</p>')
email.send()

# This will send text- and html email, will convert text to html using Markdown
email = Email('to@example.com', 'Subject', 'Line one\n\nLine two')
email.send(text=True, html=True)

# This will send html email only
email = Email('to@example.com', 'Subject', html_body='<p>Line one</p><p>Line two</p>')
email.send()

# This will send text- and html email, will convert html to text by removing html tags, converting paragraphs and breaks
email = Email('to@example.com', 'Subject', html_body='<p>Line one</p><p>Line two</p>')
email.send(text=True, html=True)

# This will send text email only, since there is no body given, the text must be in the templates
email = Email('to@example.com', 'Subject', text_template='email/my_text_email.html')
email.send()

# This will send html email only, since there is no body given, the text must be in the templates
email = Email('to@example.com', 'Subject', html_template='email/my_html_email.html')
email.send()

# This will send text- and html email, since there is no body given, the text must be in the templates
email = Email('to@example.com', 'Subject', text_template='email/my_text_email.html', html_template='email/my_html_email.html')
email.send()

# This will generate an error: when proving only one custom template, you can't send both email versions
email = Email('to@example.com', 'Subject', html_template='email/my_html_email.html')
email.send(text=True, html=True)

# This will generate an error: when using default templates, you need to give at least one body (text or html)
email = Email('to@example.com', 'Subject')
email.send()
"""

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from htmlrenderer import render


class BodyNotSetException(Exception):
    pass


class NothingToSendException(Exception):
    pass


class Email(object):
    to = None
    subject = None
    cc = None
    bcc = None
    from_address = None
    attachments = None

    text_body = None
    html_body = None
    text_template = None
    html_template = None

    kwargs = None

    _default_text_template = 'email/base_text_email.html'
    _default_html_template = 'email/base_html_email.html'
    _context = None
    _custom_templates = False
    _markdown = None

    def __init__(self, to=None, subject=None, text_body=None, html_body=None, attachments=[], cc=None, bcc=None,
                 from_address=None, text_template=None, html_template=None, **kwargs):
        """
        Init the class, the kwargs will be used as context variables
        """
        self.to = to
        self.subject = subject
        self.attachments = attachments
        self.cc = cc
        self.bcc = bcc
        self.from_address = from_address
        self.text_body = text_body
        self.html_body = html_body
        self.text_template = text_template
        self.html_template = html_template
        self.kwargs = kwargs

        if text_template or html_template:
            self._custom_templates = True

    def text_to_html(self):
        """
        Use Markdown to create a HTML version from the text body
        """
        if not self.text_body:
            return ''

        if not self._markdown:
            from markdown import Markdown
            self._markdown = Markdown()

        return self._markdown.convert(self.text_body)

    def html_to_text(self):
        """
        Use htmlrenderer to create a text version from HTML
        """
        if not self.html_body:
            return ''

        return render(self.html_body)

    def get_text_body(self):
        """
        Return the text body. If it doesn't exist, convert the html body to text.
        """
        return self.text_body or self.html_to_text()

    def get_html_body(self):
        """
        Return the html body. If it doesn't exist, covert the text body to html.
        """
        return self.html_body or self.text_to_html()

    def get_context(self):
        """
        Return the context to use for the body and subject
        Adds domain and site_name from the current site
        """
        if not self._context:
            site = Site.objects.get_current()
            self._context = {
                'domain': site.domain,
                'site_name': site.name,
                'text_body': self.get_text_body(),
                'html_body': self.get_html_body()
            }
            self._context.update(self.kwargs)

        return self._context

    def get_from_address(self):
        return self.from_address or settings.SERVER_EMAIL

    def get_text_template(self):
        if self._custom_templates:
            if not self.text_template:
                raise Exception('When using custom templates, you need to provide both the text- and the html versions')

            return self.text_template

        return self._default_text_template

    def get_html_template(self):
        if self._custom_templates:
            if not self.html_template:
                raise Exception('When using custom templates, you need to provide both the text- and the html versions')

            return self.html_template

        return self._default_html_template

    def get_rendered_text(self):
        context = {'body': self.get_text_body()}
        context.update(self.get_context())
        return render_to_string(self.get_text_template(), context)

    def get_rendered_html(self):
        context = {'body': self.get_html_body()}
        context.update(self.get_context())
        return render_to_string(self.get_html_template(), context)

    def _validate_list(self, lst):
        """
        Make sure we end up with a list
        """
        if not lst:
            return []
        if isinstance(lst, basestring):
             return [lst]
        return list(lst)

    def create_message(self, send_text, send_html):
        """
        Create a message object and return it, or return None if no recipients
        """

        # We need at least one recipient
        to = self._validate_list(self.to)
        if not len(to):
            return None

        if not send_text and not send_html:
            return None

        text = self.get_rendered_text() if send_text else None
        html = self.get_rendered_html() if send_html else None

        message = EmailMultiAlternatives(
            subject=self.subject,
            from_email=self.get_from_address(),
            to=to,
            cc=self._validate_list(self.cc),
            bcc=self._validate_list(self.bcc)
        )

        if text:
            message.body = text

            if send_html:
                # Text plus html
                message.attach_alternative(html, 'text/html')
        else:
            # There is no text version, so send it as pure html only
            message.body = html
            message.content_subtype = 'html'

        for attachment in self.attachments:
            message.attach_file(attachment)

        return message

    def send(self, text=None, html=None, fail_silent=False):
        """
        Creates a message object and sends it.
        """

        # We will send text email if text is forced, or if there is a custom text_template.
        # Otherwise only if text_body is set.
        send_text = text
        if text is None:
            send_text = bool(self.text_template) or bool(self.text_body)

        # We will send html email if html is forced, or if there is a custom html_template.
        # Otherwise only if html_body is set.
        send_html = html
        if html is None:
            send_html = bool(self.html_template) or bool(self.html_body)

        if not send_text and not send_html:
            if fail_silent:
                return False
            raise NothingToSendException('Nothing to send')

        # If we are using default templates, then text_body is required when we want to send text email,
        # and html_body is required when we want to send html email
        if not self._custom_templates:
            if send_text and not (self.text_body or self.html_body):
                raise BodyNotSetException('When using the default email templates, and you want to send text, you will need to provide a body (either text_body or html_body)')

            if send_html and not (self.html_body or self.text_body):
                raise BodyNotSetException('When using the default email templates, and you want to send html, you will need to provide a body (either text_body or html_body)')

        message = self.create_message(send_text, send_html)
        if message:
            message.send()
            return True
        return False
