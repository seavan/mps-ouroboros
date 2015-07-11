# encoding: utf-8

import json
import traceback

import redis
import bottle
import eventlet
import requests

from .logger import *

eventlet.monkey_patch()

class Ouroboros(object):
    def __new__(cls, *args, **kwargs):
        obj = super(Ouroboros, cls).__new__(cls, *args, **kwargs)
        bottle.get("/status.json")(obj.http_status_handler)
        return obj

    def __init__(self, config):
        self.config = config
        self.status = {}
        self.db = redis.StrictRedis(host=config['redis']['host'],
                                    port=config['redis']['port'],
                                    db=config['redis']['db'])

    def http_status_handler(self):
        r = bottle.HTTPResponse(status=200, body=self.status)
        r.add_header('Content-Type', 'application/json')
        return r

    def notify(self, uri, data, headers={'Content-Type': 'application/json'}, timeout=2):
        try:
            with eventlet.timeout.Timeout(timeout):
                return requests.post(uri, data=json.dumps(data), headers=headers)
        except eventlet.timeout.Timeout as e:
            error("disconnected by timeout `{0}`".format(uri))
        except requests.ConnectionError:
            error("connection error `{0}`".format(uri))

        return None

    def main(self):
        while True:
            try:
                task = self.db.lpop(self.config['redis']['queue_name'])
                if task is None:
                    eventlet.sleep(self.config['timeout'])
                    continue

                info("load task from queue: {0}".format(task))

                # TODO: validation
                task = json.loads(task)

                r = self.notify(task['uri'], task['body'])

                if r is None or r.status_code / 100 != 2:
                    warn("save task back to queue: {0}".format(task))
                    self.db.rpush(self.config['redis']['queue_name'],
                        json.dumps(task))
                else:
                    info("callback successfully sent")
            except Exception as e:
                error("unhandled exception caught: {0}".format(traceback.format_exc()))

            eventlet.sleep(self.config['timeout'])

    def run_main(self):
        eventlet.spawn_n(self.main)

    def run_http_server(self):
        bottle.run(host=self.config['http']['bind'],
            port=int(self.config['http']['port']), server='eventlet')

    def run(self):
        self.run_main()
        self.run_http_server()
