import requests
import json

class HHPosts:

	def __init__(self, access_token, limit=10):
		self.group_id = '759985267390294'
		self.limit = limit
		self.access_token = access_token


	def getPosts(self):
		r = requests.get('https://graph.facebook.com/v2.8/'+self.group_id+'/feed?access_token='+self.access_token+'&limit='+str(self.limit))
		raw = json.loads(r.text)

		posts = '{ "posts": ['

		for raw_post in raw['data']:
			post_id = raw_post['id']
			user = self.getPostUser(post_id)
			try:
				message = raw_post['message']
			except:
				continue
			time = raw_post['updated_time']

			post = '  {  "id":"'+post_id+'", "message":"'+message+'", "time":"'+time+'", '+user+'  },  '

			# print post[:-1]

			posts += post
	
		
		posts = posts[:-1]

		posts += '] }'

		return posts

		# self.save('hhposts.json', posts)




	def getPostUser(self, post_id):
		r = requests.get('https://graph.facebook.com/v2.8/'+post_id+'?fields=from&access_token='+self.access_token)
		raw = json.loads(r.text)
		name = raw['from']['name']
		user_id = raw['from']['id']
		# profile = self.getProfilePicture(user_id)
		# return ' "user": { "name": "'+name+'", "profile": "'+profile+'", "id": "'+user_id+'" } '
		return ' "user": { "name": "'+name+'", "id": "'+user_id+'" } '


	def getProfilePicture(self, user_id):
		r = requests.get('https://graph.facebook.com/v2.8/'+user_id+'?fields=picture&access_token='+self.access_token)
		raw = json.loads(r.text)
		return raw['picture']['data']['url']


	def save(self, file_name, content, option="w"):
		f = open(file_name, option)
		f.write(content)
		f.close()
			




