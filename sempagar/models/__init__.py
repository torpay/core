# -*- coding: utf-8 -*-
import sempagar
from sempagar.utils import Response
import json
import smtplib
import datetime
import sys
sys.dont_write_bytecode = True

class Model(object):
	def __init__(self, *args, **kwargs):
		self.session_instance = sempagar.application.settings['redis']
		self.access_token = None
		if len(args) > 0:
			self.access_token = args[0]
		if 'access_token' in kwargs:
			self.access_token = kwargs['access_token']
	def get_user(self):
		if self.access_token is None:
			return None
		user = self.session_instance.get('session/%s' % self.access_token)
		return json.loads(user)
	def send_valitdation_email(self, **kwargs):
		toaddr = kwargs.get('to')
		full_name = kwargs.get('full_name')
		token = kwargs.get('token')
		value = kwargs.get('value')
		fromaddr = 'sempagar.no-reply@gmail.com'
		toaddrs  = toaddr
		body_parts = []
		body_parts.append('Hello %s' % full_name)
		body_parts.append('Valor do pagamento: %s' % unicode(value))
		body_parts.append('data do pagamento: %s' % unicode(datetime.datetime.now()))
		body_parts.append('Obrigado,')
		body_parts.append('Time SemPagar')
		body = '\n'.join(body_parts)
		msg_parts = []
		msg_parts.append('Date:%s' % str(datetime.datetime.now()))
		msg_parts.append('Content-Type:text/plain')
		msg_parts.append('Subject: [SemPagar] Confirmação de pagamento')
		msg_parts.append('From:%s' % fromaddr)
		msg_parts.append('To:%s', toaddr)
		msg_parts.append(body)
		msg = '\r\n'.join(msg_parts)
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login('no-reply@goldark.com.br', '1q@W3e$R')
		server.sendmail(fromaddr, toaddrs, msg)
		server.quit()
	def render(self, status, contents, **kwargs):
		mimetype = kwargs.get('mimetype')
		if mimetype is None:
			mimetype = 'json'
		charset = kwargs.get('charset')
		if charset is None:
			charset = 'utf8'
		response = Response()
		response.set_content_type(mimetype)
		response.set_charset(charset)
		response.status = status
		response.response = contents
		return response
