#!/usr/bin/env python3
# coding:utf-8
# Copyright 2017 Scout Exchange, LLC. All Rights Reserved.
from flask import Flask, jsonify, request


app = Flask(__name__)
# we should test request tokens to make sure they came from slack.
app.config['token'] = '3TXXJyr3EHFhDDMTqDT2TlPl'


@app.route('/test-hook', methods=['POST'])
def test_hook():
    response = {
        'text': 'test-hook response; *ngrok worked*!'
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)