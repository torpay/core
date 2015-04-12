# -*- coding: utf-8 -*-
from sempagar.utils import request
import config
import json
import copy
import sys
sys.dont_write_bytecode = True

def signup(data):
	_data = copy.copy(data)
	if type(_data) != dict:
		_data = json.loads(data)
	url = '%s/users' % (config.host)
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='POST', headers=headers, mimetype='json', data=_data)
def login(data):
	_data = copy.copy(data)
	if type(_data) != dict:
		_data = json.loads(data)
	url = '%s/sessions' % (config.host)
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='POST', headers=headers, mimetype='json', data=_data)

def logout(access_token):
	url = '%s/sessions' % (config.host)
	headers = {
		'X-Access-Token': access_token,
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='DELETE', headers=headers)

def get(phone_number):
	url = '%s/users?phone=%s' % (config.host, phone_number.replace('+', '%2B'))
	print url
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='GET', headers=headers)

def get_profile(user_id):
	url = '%s/users/%s' % (config.host, user_id)
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='GET', headers=headers)

def update_profile(user_id, data):
	_data = copy.copy(data)
	if type(_data) != dict:
		_data = json.loads(data)
	url = '%s/users/%s' % (config.host, user_id)
	headers = {
		'X-Api-Token': config.api_token
	}
	return request(url=url, method='PUT', headers=headers, mimetype='json', data=_data)
