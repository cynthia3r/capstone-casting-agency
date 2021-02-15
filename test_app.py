
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db, Movie, Actor, db_drop_and_create_all


casting_assistant_jwt = "Bearer {}".format(os.environ.get('CASTING_ASSISTANT_JWT'))
casting_director_jwt = "Bearer {}".format(os.environ.get('CASTING_DIRECTOR_JWT'))
executive_producer_jwt = "Bearer {}".format(os.environ.get('EXECUTIVE_PRODUCER_JWT'))


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = os.environ['TEST_DATABASE_URL']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # drop and create all tables
            db_drop_and_create_all()

        # sample actor to be used for test
        self.new_actor_1 = {
            'name': 'Gal Gadot',
            'gender': 'female',
            'age': 35,
        }
        self.new_actor_2 = {
            'name': 'Daisy Ridley',
            'gender': 'female',
            'age': 30,
        }

        self.update_actor = {
            'name': 'Daisy Ridley',
            'gender': 'female',
            'age': 28,
        }

        self.new_movie_1 = {
            'title': 'Mission: Impossible 7',
            'release_date': '2021-11-19',
        }

        self.new_movie_2 = {
            'title': 'Matrix',
            'release_date': '2021-12-22',
        }

        self.update_movie = {
            'title': 'The Matrix 4',
            'release_date': '2021-12-22',
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation
    and for expected errors.
    """

    """
    Test API endpoint for actors
    """

    def test_post_actors(self):
        res = self.client().post('/actors', json=self.new_actor_1, headers={"Authorization": (casting_director_jwt)})
        data = json.loads(res.data)

        # check status and status message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['actor'])

    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": (casting_assistant_jwt)})
        data = json.loads(res.data)

        # check status and status message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(len(data['actors']) >= 0)

    def test_patch_actors(self):
        res = self.client().post('/actors', json=self.new_actor_1, headers={"Authorization": (executive_producer_jwt)})
        res = self.client().patch('/actors/1', json=self.update_actor, headers={"Authorization": (executive_producer_jwt)})
        data = json.loads(res.data)

        # check status and status message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(len(data['actor']) == 1)

    def test_delete_actors(self):
        res = self.client().post('/actors', json=self.new_actor_1, headers={"Authorization": (executive_producer_jwt)})
        res = self.client().post('/actors', json=self.new_actor_2, headers={"Authorization": (executive_producer_jwt)})
        res = self.client().delete('/actors/2', headers={"Authorization": (executive_producer_jwt)})
        data = json.loads(res.data)

        # check status and status message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['delete'] == 2)

    """
    Test API endpoint for movies
    """
    def test_post_movies(self):
        res = self.client().post('/movies', json=self.new_movie_1, headers={"Authorization": (executive_producer_jwt)})
        data = json.loads(res.data)

        # check status and status message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['movie'])

    def test_get_movies(self):
        res = self.client().get('/movies', headers={"Authorization": (casting_assistant_jwt)})
        data = json.loads(res.data)

        # check status and status message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(len(data['movies']) >= 0)

    def test_patch_movies(self):
        res = self.client().post('/movies', json=self.new_movie_2, headers={"Authorization": (executive_producer_jwt)})
        res = self.client().patch('/movies/1', json=self.update_movie, headers={"Authorization": (executive_producer_jwt)})
        data = json.loads(res.data)

        # check status and status message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(len(data['movie']) == 1)

    def test_delete_movies(self):
        res = self.client().post('/movies', json=self.new_movie_1, headers={"Authorization": (executive_producer_jwt)})
        res = self.client().post('/movies', json=self.new_movie_2, headers={"Authorization": (executive_producer_jwt)})
        res = self.client().delete('/movies/2', headers={"Authorization": (executive_producer_jwt)})
        data = json.loads(res.data)

        # check status and status message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        self.assertTrue(data['delete'] == 2)

    """
    Test Error behaviour for /actors
    """

    # Test non-existent actor
    def test_404_get_request_non_existent_actor(self):
        res = self.client().get('/actors/1000', headers={"Authorization": (executive_producer_jwt)})
        data = json.loads(res.data)

        # check status and status message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test non-existent actor update
    def test_404_update_actors(self):
        res = self.client().patch('/actors/1000', json=self.update_actor, headers={"Authorization": (executive_producer_jwt)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    # Test non-existent actor deletion
    def test_404_delete_request_non_existent_actor(self):
        res = self.client().delete('/actors/1599', headers={"Authorization": (executive_producer_jwt)})
        data = json.loads(res.data)

        # check status and status message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test get actor without RBAC permission
    def test_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # Test actor creation without RBAC permission
    def test_401_post_actors(self):
        res = self.client().post('/actors', json=self.new_actor_2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    """
    Test Error behaviour for /movies
    """

    # Test non-existent movie
    def test_404_get_request_non_existent_movie(self):
        res = self.client().get('/movies/1000', headers={"Authorization": (executive_producer_jwt)})
        data = json.loads(res.data)

        # check status and status message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test non-existent movie update
    def test_404_patch_movies(self):
        res = self.client().patch('/movies/1500', json=self.update_movie, headers={"Authorization": (executive_producer_jwt)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    # Test non-existent movie deletion
    def test_404_delete_request_non_existent_movie(self):
        res = self.client().delete('/movies/1500', headers={"Authorization": (executive_producer_jwt)})
        data = json.loads(res.data)

        # check status and status message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test get actor without RBAC permission
    def test_401_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    # Test movie creation without RBAC permission
    def test_401_post_movies(self):
        res = self.client().post('/movies', json=self.new_movie_2)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
