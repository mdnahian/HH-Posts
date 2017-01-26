from flask import Flask, render_template
from flask_ask import Ask, statement, session
from posts import HHPosts
import json

app = Flask(__name__)
ask = Ask(app, '/')

ACCESS_TOKEN = '394481284233235|JSbBUZApb9IvMm_JLeN0_3L5p60'
hh = HHPosts(ACCESS_TOKEN, 9)


def buildResponse(posts, start, stop):
	response = ''
	count = 0
	session.attributes['stop'] = stop
	for post in posts['posts']:
		if count > start & count < stop:
			response = response + post['user']['name'] + ' posted ' + response['message'] + '. '
		count += 1
	return response


@app.route('/')
	return 'HH Posts Skills Running...'


@ask.launch
def launch():
	session.attributes['posts'] = hh.getPosts()
	posts = json.loads(session.attributes['posts'])
	response = buildResponse(posts, 0, 2)
	
	if response != '':
		return question(response+' Say Next if you want me to read more posts.')
	else:
		return statement(render_template('error'))


@ask.intent('NextPostsIntent')
def nextPosts():
	posts = json.loads(session.attributes['posts'])
	start = session.attributes['stop'] + 1
	stop = session.attributes['stop'] + 3
	if stop < 9:
		response = buildResponse(posts, start, stop)
		return question(response+' Say Next if you want me to read more posts.')
	else:
		return statement(render_template('finished'))




@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Goodbye")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Goodbye")


@ask.intent('AMAZON.HelpIntent')
def help():
	return statement(render_template('help'))



if __name__ == '__main__':
	app.run()
