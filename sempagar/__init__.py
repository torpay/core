# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import pymongo
import redis
import utils
import sdks
import config
import handlers
import sys
sys.dont_write_bytecode = True

mongo = pymongo.MongoClient()
redis = redis.StrictRedis()

routes = []
#users
routes.append((r'/users', handlers.Users))
routes.append((r'/users/login', handlers.UserSession))
routes.append((r'/users/logout', handlers.UserSession))
routes.append((r'/users/profile', handlers.UserProfile))

application = tornado.web.Application(routes, mongo=mongo, redis=redis, debug=True)

def run(port=5000):
	print 'Starting ark server....'
	application.listen(port)
	print 'Running on port %s' % port
	tornado.ioloop.IOLoop.instance().start()
