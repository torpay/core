import simplify
import config
import creditcard as creditcard

simplify.public_key = config.simplify_access['public_key']
simplify.private_key = config.simplify_access['private_key']

def tokenify(card):
	obj = {
		"card" : card
	}
	try:
		cardToken = simplify.CardToken.create(obj)
		token_id = cardToken.id if cardToken else None
	except: 
		token_id = None

	return token_id

def charge_with_token( token, currency, amount, description=None):

	obj = {
		"token" : token,
		"amount" : amount,
		"description" : description,
		"currency" : currency
	}
	if description:
		obj['description'] = description

	payment = simplify.Payment.create( obj )

	if payment.paymentStatus == 'APPROVED':
		print "Payment approved"

	return payment

def charge_with_card_details(card, currency, amount, description=None):

# amount [min value: 50, max value: 9999900]
# currency [default: USD]
# description [max length: 1024]
	amount = unicode(amount)
	if len(amount) <= 2:
		amount = '%s0' % amount
	obj = {
		"card" : card,
		"amount" : amount,
		"description" : description,
		"currency" : currency
	}
	if description:
		obj['description'] = description
	try:
		payment = simplify.Payment.create( obj )
	except Exception as e:
		print '---'
		print amount
		print e.error_code
		for _e in e.field_errors:
			print _e
		print '---'
		ieda()

	if payment.paymentStatus == 'APPROVED':
		print "Payment approved"

	return payment


def test_charge_with_card():
	card = creditcard.CreditCard(number = '5105105105105100', exp_month='06' , exp_year='20', cvc='123')
	receipt = charge_with_card_details(amount = 100, description = "shipment of two eggs in a glass bottle" , currency = "USD", card=card.to_simplify_obj())
	print "Callback returned: %s" % receipt

def test_tokenify():
	card = creditcard.CreditCard(number = '5105105105105100', exp_month='06' , exp_year='20', cvc='123')
	token = tokenify( card.to_simplify_obj() )
	print " Token returned: %s" % token

def test_charge_with_token():
	card = creditcard.CreditCard(number = '5105105105105100', exp_month='06' , exp_year='20', cvc='123')
	token = tokenify( card.to_simplify_obj() )
	receipt = charge_with_token(token=token, currency="USD", amount="1000")
	print "Callback returned: %s " % receipt


if __name__ == "__main__":
	test_tokenify()
	test_charge_with_token()
	test_charge_with_card()