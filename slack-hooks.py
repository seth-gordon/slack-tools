#!/usr/bin/env python
# coding:utf-8
# Copyright 2017 Scout Exchange, LLC. All Rights Reserved.
import json
import requests
from flask import Flask, jsonify, request


app = Flask(__name__)
app.config['port'] = 4000
# we should check request tokens to make sure they came from slack.
app.config['token'] = '3TXXJyr3EHFhDDMTqDT2TlPl'

BUILD_INFO_URLS = {
    'connect': 'https://{env}-connect.goscoutgo.com/deployment_info.json',
    'tpx': 'https://{env}.talentpx.com/deployment_info.json'
    }


@app.route('/test-hook', methods=['POST'])
def test_hook():
    response = {
        'text': 'test-hook response; *ngrok worked*!'
    }
    return jsonify(response)


@app.route('/deploy', methods=['POST'])
def slack_deploy():
    response = {
        'text': 'Deploying'
    }
    return jsonify(response)


@app.route('/reload', methods=['POST'])
def slack_reload():
    response = {
        'text': 'Reloading'
    }
    return jsonify(response)


@app.route('/rollforward', methods=['POST'])
def slack_rollforward():
    response = {
        'text': 'Rolling Forward'
    }
    return jsonify(response)


@app.route('/scheduler', methods=['POST'])
def slack_scheduler():
    response = {
        'text': 'Scheduler'
    }
    return jsonify(response)


@app.route('/worker', methods=['POST'])
def slack_worker():
    response = {
        'text': 'Worker'
    }
    return jsonify(response)


@app.route('/deployment-info', methods=['POST'])
def slack_deployment_info():
    """
    Fetches connect and tpx deployment info for a given environment.
    """
    # TODO: Need to add error handling in case the environment given doesn't
    # exist in our dict.
    text = request.form['text'].strip()
    environment = text.split(' ')[0].lower()

    info = _get_deployment_info(environment)
    return jsonify(info)


def _get_deployment_info(environment):
    # TODO: Need to add error handling in case the environment given doesn't
    # exist in our dict.
    connect = requests.get(BUILD_INFO_URLS['connect'].format(env=environment))
    tpx = requests.get(BUILD_INFO_URLS['tpx'].format(env=environment))
    info = {'connect': json.loads(connect.text),
            'tpx': json.loads(tpx.text)
            }
    return info


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['port'])
