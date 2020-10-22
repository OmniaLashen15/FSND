
import os
import unittest
import json
#from sqlalchemy import Column, String, Integer, create_engine, DateTime
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor

class CastingAgencyCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency"
        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgres://{}:{}@{}/{}".format(
        'postgres', '123', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        #self.assistance_token = 'Bearer' + os.environ['assistant']
        #self.director_token = 'Bearer' + os.environ['assistant']
        #self.producer_token = 'Bearer' + os.environ['assistant']


        self.assistance_token = 'Bearer' + str(os.getenv('assistant'))
        self.director_token = 'Bearer' + str(os.getenv('director'))
        self.producer_token = 'Bearer' + str(os.getenv('producer'))

        self.assistance_header = {'Authorization': self.assistance_token}
        self.director_header = {'Authorization':self.director_token}
        self.producer_header = {'Authorization':self.producer_token}     
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = {
            'id':5,
            'name':'Emilia Clark',
            'age':33,
            'gender':'female'
        }

    

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_for_non_existing_actors(self):
        res = self.client().get('/actors/', headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_sent_requesting_for_non_existing_movies(self):
        res = self.client().get('/movies/', headers=self.director_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_actor(self):
        res = self.client().delete('/actors/3', headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
        
    def test_422_if_deleted_actor_not_exist(self):
        res = self.client().delete('/actors/5000', headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    
    def test_422_if_deleted_movie_not_exist(self):
        res = self.client().delete('/movies/5000', headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    def test_delete_movies(self):
        res = self.client().delete('/movies/2', headers=self.producer_header)
        data = json.loads(res.data)
        #actor = Actor.query.filter(Actor.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        
    
    def test_post_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)

    def test_400_if_created_actor_bad_request(self):
       
       res = self.client().post('/actors', json={'name':'' ,'gender':''}, headers=self.producer_header)
       data = json.loads(res.data) 
       self.assertEqual(res.status_code, 400)
       self.assertEqual(data['success'], False)
       self.assertEqual(data['message'], 'bad request') 
    
    
    def test_post_movies(self):
        new_movie = {'title':'greenland','release_date':'23/9/2020','movie_id':10} 
        res = self.client().post('/movies', json=new_movie, headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        
    
    def test_400_if_created_movie_bad_request(self):
       res = self.client().post('/movies', json={ }, headers=self.producer_header)
       data = json.loads(res.data) 
       self.assertEqual(res.status_code, 400)
       self.assertEqual(data['success'], False)
       self.assertEqual(data['message'], 'bad request')

    def test_patch_actor(self):
        res = self.client().patch('/actors/3', json={'age':22}, headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    def test_patch_actor_not_found(self):
        res = self.client().patch('/actors/89', headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_patch_movie(self):
        res = self.client().patch('/movies/25', json={'title':'law abiding citizen'},headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    def test_patch_movie_not_found(self):
        res = self.client().patch('/movies/75',headers=self.producer_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found') 
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
