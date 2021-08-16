import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from config import (
    database_param,
    EXECUTIVE_PRODUCER,
    CASTING_ASSISTANT,
    CASTING_DIRECTOR
)


# Assign testing authorization headers

# database path
database_path = os.environ.get('DATABASE_URL',
                               "{}://{}:{}@localhost: 5432/{}".format(
                                   database_param["dialect"],
                                   database_param["username"],
                                   database_param["password"],
                                   database_param["db_name"]))


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.test_movie = {
            "title": "qwerty",
            "release_date": "1987.06.05"
        }
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # test cases
    # ACTORS
    def test_add_actors(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Kafilat', 'age': '23', 'gender': 'female'},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['actor'])

    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # test get movies
    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers={"Authorization": "Bearer " +
                                         CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_400_create_actor(self):
        new_actor = {
            "name": "",
            "age": 24,
            "gender": "erkak"
        }
        res = self.client().post('/actors', json=new_actor,
                                 headers={"Authorization": "Bearer " +
                                          EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # test create movie

    def test_create_movie(self):
        new_movie = {'title': 'New_Movie_1',
                     'release_date':
                     '12/6/2020'}
        res = self.client().post('/movies', json=new_movie,
                                 headers={"Authorization": "Bearer " +
                                          EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_post_movie(self):
        response = self.client().post(
            '/movies',
            json={
                "title": ""
            },
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # test delete actor

    def test_delete_actor(self):
        actor = Actor.query.all()[-1]
        response = self.client().delete(
            '/actors/'+str(actor.id),
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delete_actor(self):
        res = self.client().delete(
            '/actors/400', headers={"Authorization": "Bearer " +
                                    CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            "resource not found")

    # test delete movie

    def test_delete_movie(self):
        movie = Movie.query.all()[-1]
        response = self.client().delete(
            '/movies/'+str(movie.id),
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    def test_404_delete_movie(self):
        response = self.client().delete(
            '/movies/22321',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # test update actor

    def test_update_actor(self):
        update_actor = {'name': 'Abdurahim'}
        res = self.client().patch('/actors/3', json=update_actor,
                                  headers={"Authorization": "Bearer " +
                                           CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_patch_actor(self):
        response = self.client().patch(
            '/actors/10',
            json={

            },
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    def test_404_patch_actor(self):
        response = self.client().patch(
            '/actor/12323',
            json={'name': 'Johnathan', 'age': 25, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # test update movie

    def test_update_movie(self):
        update_movie = {'title': 'UPDATE_NAME',
                        'release_dat': '12/6/2020'
                        }
        res = self.client().patch('/movies/10', json=update_movie,
                                  headers={"Authorization":
                                           "Bearer " + CASTING_DIRECTOR})
        # print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_patch_movie(self):
        response = self.client().patch(
            '/movies/12323',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # RBAC remaining tests
    # Casting assistant
    def test_get_actors_casting_assistant(self):
        res = self.client().get('/actors',
                                headers={"Authorization":
                                         "Bearer " + CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_update_movie_casting_assistant(self):
        update_movie = {'title': 'UPDATE_NAME',
                        'release_dat': '12/6/2020'
                        }
        res = self.client().patch('/movies/2', json=update_movie,
                                  headers={"Authorization":
                                           "Bearer " + CASTING_ASSISTANT})
        # print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "unauthorized")

    def test_create_movie_casting_assistant(self):
        new_movie = {'title': 'New_Movie_1', 'release_date': '12/6/2020'}
        res = self.client().post('/movies', json=new_movie,
                                 headers={"Authorization": "Bearer " +
                                          CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Permission not found.")

    # Casting Director
    def test_get_actors_casting_director(self):
        res = self.client().get('/actors',
                                headers={"Authorization": "Bearer " +
                                         CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_create_movie_casting_assistant(self):
        new_movie = {'title': 'New_Movie_1', 'release_date': '12/6/2020'}
        res = self.client().post('/movies', json=new_movie,
                                 headers={"Authorization": "Bearer " +
                                          CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "unauthorized")

    def test_delete_movie_casting_director(self):
        res = self.client().delete('/movies/5',
                                   headers={"Authorization":
                                            "Bearer " + CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "unauthorized")

    # Executive producer RBAC tests are covered above


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
