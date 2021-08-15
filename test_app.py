import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from config import  database_param


EXECUTIVE_PRODUCER ="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhxeEJXY180aU1jWG9EWTA2REotRiJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLTc0MDQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMTc4ZDYwODFkOTliMDA3MGVmNWE3NCIsImF1ZCI6ImNhcHN0b25lLWFwaSIsImlhdCI6MTYyOTAyMzE5NSwiZXhwIjoxNjI5MTA5NTk1LCJhenAiOiJQU1J3MTROU2dQb1dpSXFMM3A0UjU2czJsY3JFM2UxbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiXX0.fNvl3o3Db4pU8T1s3tdGjKpkos-_76uB3TMDRiVIcqa6boyZr5m14oJr4kQli5aAYerlKa5bz6CrgzALi_y4OZ3e-cTFXnxtqgOQ2TogLnhKK1UEnh-YrsC8fqk-8uxcRysOiOjx205riOTEG4zduhGtt5eF-LGutpR1wChZ829EFo6UnycHnQE8ZFncId5DmO1ocxs8N7FlIXiCsbLLhGkzdJWNXdWHczpqLpeXYaQ-ytyj_us37d2rNfc19y6_hRFyQIReka-BjodB4ymYyLOUL370IN93_Y4iGamO4YbcQ69XKwFwX3-S3POgPWk_LExaOg5mCdkWQe3XqdtRzw"
CASTING_ASSISTANT ="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhxeEJXY180aU1jWG9EWTA2REotRiJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLTc0MDQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMTdmNTA5NTIwOTY2MDA3MDdhOGZiZSIsImF1ZCI6ImNhcHN0b25lLWFwaSIsImlhdCI6MTYyOTAyNjQwNiwiZXhwIjoxNjI5MTEyODA2LCJhenAiOiJQU1J3MTROU2dQb1dpSXFMM3A0UjU2czJsY3JFM2UxbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.dgKBwRZKtgK8NFPXgCj_H1IST3JoY_mSIvgduIYCT-vhlekk8V7Q9EYkdlGvGNsHMdTQqkoaE4wbqX4TId_kms1173VfGVEoBo3_vR0i0Wf7EMv7N971dZeQPuC9kfleRkRt-kIdeTi0su-j4NKvoHdTAVXcn6-zbtLW08IPj1hNe-ckiIXrNG4R-Zzz_8OvHGGfTM2zimQZOJ2-ER6TEMfjUXDcQ5K9mYada5u32gyNIsNDY98BsDm1PNJ8j69p39Hv7YP3PS62BzabVo0Iu7rht-0vTKweCr4_XZWdnEOxqs9FWe1f_5ApiNY4d45imwqIeQ6gWgFIPXs65QbV6w"
CASTING_DIRECTOR ="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhxeEJXY180aU1jWG9EWTA2REotRiJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLTc0MDQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMTdmM2RiMjAxYzJlMDA2OTg1NjVkYyIsImF1ZCI6ImNhcHN0b25lLWFwaSIsImlhdCI6MTYyOTAyNjEwOSwiZXhwIjoxNjI5MTEyNTA5LCJhenAiOiJQU1J3MTROU2dQb1dpSXFMM3A0UjU2czJsY3JFM2UxbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.kwUC1aQNjt6pR6rU5Gw_Odr1PEQqRK_mg64EA1YRwpy7Q9OH2tDpccIgUyt0ka14CeDEOalLtBZeDiO8dJWVfbauE6APEX727ZZO41uvcE2tzrasNKyDO9N-nqKHcfD1TgI4FDVeE3V9VPo4q004CCS8I_r7GT-rSjY6q-xAMHsUP1qukb-QZYCCgDJO8rmClwSaSU_NdOjtQ-Fs7CUEzruC16D2j7llebrGb9YQoE23MWqAlcLm1J5kzErU_Ijg5mHxQsIpIqda_HVbfFEkaXOzzNYpXUct3SlOu3h85jxM4v9Gw26uk8XNqP40rkFdDTnoL3e0uhch_PyyrgQwwQ"
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
        self.test_movie={
            "title":"qwerty",
            "release_date":"1987.06.05"
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
    #ACTORS
    def test_add_actors(self):
        response= self.client().post(
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
                                headers={"Authorization": "Bearer " + CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))


    def test_400_create_actor(self):
        new_actor = {
            "name":"",
            "age":24,
            "gender":"erkak"
        }
        res = self.client().post('/actors', json=new_actor,
                                 headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        

    # test create movie
    def test_create_movie(self):
        new_movie = {'title': 'New_Movie_1',
                     'release_date': '12/6/2020'}
        res = self.client().post('/movies', json=new_movie,
                                 headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_post_movie(self):
        response = self.client().post(
            '/movies',
            json={
                "title":""
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
        actor=Actor.query.all()[-1]
        response = self.client().delete(
            '/actors/'+str(actor.id),
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/400', headers={"Authorization": "Bearer " + CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            "resource not found")

    # test delete movie
    

    def test_delete_movie(self):
        movie=Movie.query.all()[-1]
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
                                  headers={"Authorization": "Bearer " + CASTING_DIRECTOR})
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
        update_movie = {'title': 'UPDATE_NAME', 'release_dat': '12/6/2020'
                        }
        res = self.client().patch('/movies/10', json=update_movie,
                                  headers={"Authorization": "Bearer " + CASTING_DIRECTOR})
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
                                headers={"Authorization": "Bearer " + CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_update_movie_casting_assistant(self):
        update_movie = {'title': 'UPDATE_NAME', 'release_dat': '12/6/2020'
                        }
        res = self.client().patch('/movies/2', json=update_movie,
                                  headers={"Authorization": "Bearer " + CASTING_ASSISTANT})
        # print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "unauthorized")

    def test_create_movie_casting_assistant(self):
        new_movie = {'title': 'New_Movie_1', 'release_date': '12/6/2020'}
        res = self.client().post('/movies', json=new_movie,
                                 headers={"Authorization": "Bearer " + CASTING_ASSISTANT})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "Permission not found.")

    # Casting Director
    def test_get_actors_casting_director(self):
        res = self.client().get('/actors',
                                headers={"Authorization": "Bearer " + CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_create_movie_casting_assistant(self):
        new_movie = {'title': 'New_Movie_1', 'release_date': '12/6/2020'}
        res = self.client().post('/movies', json=new_movie,
                                 headers={"Authorization": "Bearer " + CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "unauthorized")

    def test_delete_movie_casting_director(self):
        res = self.client().delete('/movies/5',
                                   headers={"Authorization": "Bearer " + CASTING_DIRECTOR})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'], "unauthorized")

    # Executive producer RBAC tests are covered above


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
