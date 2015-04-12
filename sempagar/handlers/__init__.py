# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import tornado.gen
import json
import datetime
import sys

sys.dont_write_bytecode = True

class Handler(tornado.web.RequestHandler):
    def initialize(self):
        self.api_token = self.request.headers.get('X-Api-Token')
        self.access_token = self.request.headers.get('X-Access-Token')
        self.content_type = self.request.headers.get('Content-Type')
        self.data = self.request.body
        self.host = self.request.host
        self.args = {}
        self.app_name = ''
        self.parse_args()
        self.parse_content_type()
    def prepare(self):
        self.parse_body()
        self.is_valid_api_token()
    def parse_args(self):
        for arg in self.request.query_arguments:
            self.args[arg] =  self.request.query_arguments[arg][0]
    def parse_content_type(self):
        if  self.content_type:
            self.content_type = self.content_type.split(';')[0]
        else:
             self.content_type = ''
    def parse_body(self):
         if self.data:
            if 'json' in self.content_type:
                try:
                    self.data = json.loads(self.data)
                except Exception:
                    self.render_as_internal_error()
    def render(self, data):
        self.set_header('Content-Type', data.content_type)
        self.set_status(data.status)
        self.finish(data.render_as_json())
    def is_valid_api_token(self):
        return True
        self.parse_host()
        redis_token = self.redis.get(self.api_token_key)
        return self.api_token == redis_token
    def render_as_unauthorized(self):
        self.set_header('Content-Type', 'application/json;charset=utf-8')
        self.set_status(HTTPCode.UNAUTHORIZED)
        self.finish(json.dumps({'error': 'unauthorized'}))
    def render_as_not_allowed(self):
        self.set_header('Content-Type', 'application/json;charset=utf-8')
        self.set_status(HTTPCode.NOT_ALLOWED)
        self.finish(ujson.dumps({'error': 'http method/verb not allowed'}))
    def render_as_internal_error(self):
        self.set_header('Content-Type', 'application/json;charset=utf-8')
        self.set_status(HTTPCode.INTERNAL_ERROR)
        self.finish(ujson.dumps({'error': 'internal error'}))
    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        self.render_as_not_allowed()
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        self.render_as_not_allowed()
    @tornado.gen.coroutine
    def put(self, *args, **kwargs):
        self.render_as_not_allowed()
    @tornado.gen.coroutine
    def delete(self, *args, **kwargs):
        self.render_as_not_allowed()
    @tornado.gen.coroutine
    def options(self, *args, **kwargs):
        self.render_as_not_allowed()
    @tornado.gen.coroutine
    def head(self, *args, **kwargs):
        self.render_as_not_allowed()
    @tornado.gen.coroutine
    def trace(self, *args, **kwargs):
        self.render_as_not_allowed()
    @tornado.gen.coroutine
    def patch(self, *args, **kwargs):
        self.render_as_not_allowed()
    @tornado.gen.coroutine
    def write_error(self, status_code, **kwargs):
        self.render_as_internal_error()

from users import *
from payments import *
