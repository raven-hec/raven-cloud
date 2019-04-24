from app import app
import unittest

class FlaskappTests(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True

	def test_users_status_code(self):
		result = self.app.get('/api/v1/users')
		self.assertEqual(result.status_code, 200)

	def test_tweets_status_code(self):
		result = self.app.get('/api/v2/tweets')
		self.assertEqual(result.status_code, 200)

	def test_info_status_code(self):
		result = self.app.get('/api/v1/info')
		self.assertEqual(result.status_code, 200)

	def test_addusers_status_code(self):
		result = self.app.post('/api/v1/users', data='{"username":"manish21", "email":"manishtest@gmail.com", "password":"test123"}',
			content_type='application/json')
		print(result)
		self.assertEquals(result.status_code, 201)

	def test_updusers_status_code(self):
		result = self.app.put('/api/v1/users/1', data='{"password":"testing123"}', content_type='application/json')
		self.assertEquals(result.status_code, 200)

	def test_addtweets_status_code(self):
		result = self.app.post('/api/v2/tweets', data='{"username":"mahesh@rocks123","body":"Wow! Is it working #testing"}',
			content_type='application/json')
		self.assertEqual(result.status_code, 201)

	def test_delusers_status_code(self):
		result = self.app.delete('/api/v1/users', data='{"username":"manish21"}', content_type='application/json')
		self.assertEquals(result.status_code, 200)
