import unittest
from app import app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to MovieWeb App', response.data)

    def test_users_page(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1 class="user-header">Users</h1>', response.data)

    def test_user_details_page(self):
        user_id = 1  # Replace with an actual user ID
        response = self.app.get(f'/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1 class="user-header">User 1: Movies', response.data)

    def test_add_user(self):
        response = self.app.post('/add_user', data={'name': 'test_user2'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'test_user2', response.data)

    def test_add_duplicate_user(self):
        response = self.app.post('/add_user', data={'name': 'test_user'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User already exist', response.data)

    def test_add_new_movie(self):
        user_id = 1  # Replace with an actual user ID
        response = self.app.post(f'/users/{user_id}/add_movie', data={'title': 'Black Widow'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Black Widow', response.data)

    def test_add_duplicate_movie(self):
        user_id = 1  # Replace with an actual user ID
        response = self.app.post(f'/users/{user_id}/add_movie', data={'title': 'Titanic'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Movie already exist!', response.data)

    def test_update_movie(self):
        user_id = 1  # Replace with an actual user ID
        movie_id = "tt0371746"  # Replace with an actual movie ID
        response = self.app.post(f'/users/{user_id}/update_movie/{movie_id}',
                                 data={'title': 'Updated Movie'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Movie', response.data)

    def test_delete_movie(self):
        user_id = 1  # Replace with an actual user ID
        movie_id = "tt3480822"  # Replace with an actual movie ID
        response = self.app.get(f'/users/{user_id}/delete_movie/{movie_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
