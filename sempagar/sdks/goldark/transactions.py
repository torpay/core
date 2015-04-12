# -*- coding: utf-8 -*-
from sempagar.utils import request
import config
import json
import copy
import sys
sys.dont_write_bytecode = True

def create(data):
	_data = copy.copy(data)
	if type(_data) != dict:
		_data = json.loads(data)
	url = '%s/invoices' % (config.host)
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='POST', headers=headers, mimetype='json', data=_data)

def get(merchant_id, consumer_id, **kwargs):
	status = kwargs.get('status')
	if status is None:
		status = 'pending'
	url = '%s/invoices?merchant=%s&consumer=%s&status=%s' % (config.host, merchant_id, consumer_id, status)
	print url
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='GET', headers=headers)

def get_one(payment_id):
	url = '%s/invoices/%s' % (config.host, payment_id)
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='GET', headers=headers)

def update(payment_id, data):
	url = '%s/invoices/%s' % (config.host, payment_id)
	_data = copy.copy(data)
	if type(_data) != dict:
		_data = json.loads(data)
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='PUT', headers=headers, mimetype='json', data=_data)

def search(user_id):
	url = '%s/invoices?merchant=%s' % (config.host, user_id)
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='GET', headers=headers)

