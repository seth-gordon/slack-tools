#!/usr/bin/env python
# coding:utf-8
# Copyright 2017 Scout Exchange, LLC. All Rights Reserved.
from gevent import monkey; monkey.patch_all()
from functools import wraps
import json
import gevent.queue, gevent
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

ASYNC_RESPONSE_LIMIT = 5
ASYNC_RESPONSE_TIMEOUT = 30 * 60


def queue_consumer(response_queue, async_response_url):
    for i in range(ASYNC_RESPONSE_LIMIT):
        try:
            message = response_queue.get()
        finally:
            # we have this in a finally block so that if the
            # a GreenletExit exception is raised, we can try
            # to send this response before termination
            response = requests.post(async_response_url,
                                     json={'response_type': 'in_channel',
                                           'text': message
                                           })
            # NOTE: I'm not sure whether app can be called
            # from other threads
            app.logger.info("Message sent: %s", message)
            if response.status_code != 200:
                errmsg = ("Attempt to send async response %s "
                          "yielded status code %d")
                app.logger.error(errmsg, message, response.status_code)


def async_slash_command(f):
    # The wrapper function returns immediately, so that the Slack server
    # gets its response in the 3-second time limit.  But the wrapped
    # function continues to execute in another greenlet thread, so that
    # it can send messages asynchronously back to the user.
    @wraps(f)
    def wrapper(*args, **kwargs):
        slash_command = request.form['command']
        slash_argument_text = request.form['text']
        async_response_url = request.form['response_url']
        response_queue = gevent.queue.Queue(maxsize=ASYNC_RESPONSE_LIMIT)
        consumer_greenlet = gevent.spawn(queue_consumer,
                                         response_queue,
                                         async_response_url)
        producer_greenlet = gevent.spawn(f,
                                         slash_argument_text,
                                         response_queue,
                                         *args,
                                         **kwargs)
        # when the producer is done, so is the consumer
        producer_greenlet.link(lambda g: consumer_greenlet.kill())
        # when the Slack timeout for async response is up, kill both
        consumer_greenlet.kill(block=False, timeout=ASYNC_RESPONSE_TIMEOUT)
        producer_greenlet.kill(block=False, timeout=ASYNC_RESPONSE_TIMEOUT)
        # send the regular HTTP response that the server expects
        sync_msg_template = "OHAI this bot received a {} command with arg {}"
        sync_msg = sync_msg_template.format(slash_command, slash_argument_text)
        sync_response = {'response_type': 'in_channel',
                         'text': sync_msg}
        return jsonify(sync_response)
    return wrapper

@async_slash_command
@app.route('/test-hook', methods=['POST'])
def test_hook(slash_argument_text, response_queue):
    response_queue.put('test-hook response; *ngrok worked*! arg: ' +
                       slash_argument_text)
    response_queue.put('another test-hook response')
    response_queue.put('and another response, just to show that we can')
    response_queue.put('fourth response')
    response_queue.put('fifth response')
    response_queue.put('you should not see this in the Slack window')


@async_slash_command
@app.route('/deploy', methods=['POST'])
def slack_deploy(slash_argument_text, response_queue):
    response_queue.put('Deploying ' + slash_argument_text)
    response_queue.put('Deployment complete')

@async_slash_command
@app.route('/reload', methods=['POST'])
def slack_reload(slash_argument_text, response_queue):
    response_queue.put('Reloading ' + slash_argument_text)
    response_queue.put('Reload complete')


@async_slash_command
@app.route('/rollforward', methods=['POST'])
def slack_rollforward(slash_argument_text, response_queue):
    response_queue.put('Rolling forward ' + slash_argument_text)
    response_queue.put('Roll-forward complete')


@async_slash_command
@app.route('/scheduler', methods=['POST'])
def slack_scheduler(slash_argument_text, response_queue):
    response_queue.put('Scheduler ' + slash_argument_text)
    response_queue.put('Scheduling stuff complete')


@async_slash_command
@app.route('/worker', methods=['POST'])
def slack_worker(slash_argument_text, response_queue):
    response_queue.put('Worker ' + slash_argument_text)
    response_queue.put('Worker stuff complete')


# leave this as a purely synchronous hook for now
@app.route('/deployment-info', methods=['POST'])
def slack_deployment_info(slash_argument_text, response_queue):
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
