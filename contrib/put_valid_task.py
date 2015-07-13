#!/usr/bin/env python

import json
import redis

if __name__ == "__main__":
    db = redis.StrictRedis(host='localhost', db=1)

    task = {
        'uri': 'http://127.0.0.1:9090',
        'payload': {
            'id': 10000000000000000000,
            'status': "FAIL",
            'status_code': 10
        }
    }

    print task
    db.rpush('callbacks', json.dumps(task))
