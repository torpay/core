# -*- coding: utf-8 -*-
from sempagar.utils import request
import config
import json
import copy
import sys
sys.dont_write_bytecode = True

def find_by_consumer(user_id):

	url = '%s/invoices?consumer=%s' % (config.host, user_id)
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='GET', headers=headers)

def update_status(invoice_id, data):
	_data = data

	url = '%s/invoices/%s' % (config.host, invoice_id)
	print url
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='PUT', headers=headers, mimetype='json', data=_data)

