# -*- coding: utf-8 -*-
from sempagar.models import Model
from sempagar.sdks import goldark
from sempagar.sdks import channel
from sempagar.sdks import payment
import urlparse, urllib
import json
import sys
sys.dont_write_bytecode = True

class Payment(Model):
	def create(self, data):
		user = self.get_user()
		if user is None:
			return self.render(401, {'error': 'unauthorized'})
		if not 'value' in data:
			return self.render(400, {'error': 'request.value.not_found'})
		if not 'phone' in data:
			return self.render(400, {'error': 'request.phone.not_found'})
		data['phone'] = unicode(data['phone'])
		msg = 'Pagamento de valor %s, para confirmar responda com SIM' % unicode(data['value'])
		(consumer_response, consumer_code, consumer_mimetype) = goldark.users.get(data['phone'])
		if consumer_code == 404:
			return self.render(404, {'error': 'user.not_found'})
		parsed_consumer_response = json.loads(consumer_response)
		(response, code, mimetype) = goldark.transactions.create({
			'merchant': user['id'],
			'consumer': parsed_consumer_response['data'][0]['id'],
			'status': 'pending',
			'description': data.get('description'),
			'currency': 'BRL',
			'total_value': data['value']
		})
		if code != 201:
			return self.render(code, json.loads(response))
		channel.twilioservice.send_sms(msg, data['phone'], user['phone'])
		output = {
			'channel': {
				'msg': msg,
				'phone': user['phone']
			},
			'transaction': json.loads(response)
		}
		return self.render(201, {'msg': msg, 'to': user['phone']})
	def accept_payment(self, data):
		data = urlparse.parse_qs(data)
		answer = data.get('Body')
		phone_from = data.get('From')
		phone_to = data.get('To')
		if not answer or not phone_to or not phone_from:
			return self.render(500, {'error': 'internal.error'})
		answer = answer[0]
		phone_from = phone_from[0]
		phone_to = phone_to[0]
		(merchant_response, merchant_code, merchant_mimetype) = goldark.users.get(phone_from)
		(consumer_response, consumer_code, consumer_mimetype) = goldark.users.get(phone_to)
		print phone_to
		if merchant_code != 200:
			return self.render(404, {'error': 'merchant.not_found'})
		if consumer_code != 200:
			return self.render(404, {'error': 'consumer.not_found'})
		merchant = json.loads(merchant_response)['data'][0]
		consumer = json.loads(consumer_response)['data'][0]
		print consumer
		(response, code, mimetype) = goldark.transactions.get(merchant['id'], consumer['id'], status='pending')
		print response
		if code == 404:
			return self.render(404, {'error': 'transaction.not_found'})
		if answer.lower() != 'sim':
			goldark.transactions.update(response['id'], {'status': 'error', 'status_message': 'denied'})
			return self.render(403, {'error': 'permission denied'})
		parsed_response = json.loads(response)
		parsed_response = parsed_response['data'][0]
		(card_response, card_code, card_mimetype) = goldark.cards.get(consumer['id'])
		if card_code == 404:
			return self.render(404, {'error': 'card.not_found'})
		parsed_card_response = json.loads(card_response)
		parsed_card_response = parsed_card_response['data'][0]
		#////
		card = payment.creditcard.CreditCard(number=parsed_card_response['number'], exp_month=parsed_card_response['month'], exp_year=parsed_card_response['year'], cvc=parsed_card_response['cvc'])
 		#charged = payment.charge_with_card_details(parsed_card_response['number'], 'BRL', unicode(parsed_response['total_value']))
 		currency = parsed_response.get('curreny')
 		if currency is None:
 			currency = 'USD'
 		description = parsed_response.get('description')
		payment.simplifyservice.charge_with_card_details(card=card.to_simplify_obj(), currency= currency, amount=parsed_response['total_value'], description=description)

		goldark.transactions.update(parsed_response['id'], {'status': 'approved'})
		parsed_response['status'] = 'approved'
		goldark.push.send(merchant['id'], json.dumps(parsed_response))
		try:
			self.send_valitdation_email(to=consumer['username'], full_name=consumer.get('name'), value=parsed_response['total_value'])
		except Exception as e:
			print 'error while sending validation email'

		msg = 'Pagamento de %s confirmado.' % unicode(parsed_response['total_value'])
		print msg
		channel.twilioservice.send_sms(msg, consumer['phone'], merchant['phone'])
		return self.render(200, {'status': 'success'})
	def search(self):
		user = self.get_user()
		if user is None:
			return self.render(401, {'error': 'unauthorized'})
		(response, code, mimetype) = goldark.transactions.search(user['id'])
		return self.render(code, json.loads(response))
	def get_one(self, payment_id):
		user = self.get_user()
		if user is None:
			return self.render(401, {'error': 'unauthorized'})
		(response, code, mimetype) = goldark.transactions.get_one(payment_id)
		return self.render(code, json.loads(response))
