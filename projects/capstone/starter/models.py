import os
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

database_name = "casting_agency"
database_path = "postgres://{}:{}@{}/{}".format('postgres', '123', 'localhost:5432', database_name)
#database_path = os.getenv('Database_URL')
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)

'''
Movies

'''
class Movie(db.Model):
      __tablename__ = 'movies'

      id = Column(Integer, primary_key=True)
      title = Column(String)
      release_date = Column(DateTime)
      movie_id = Column(Integer, ForeignKey('actors.id'), nullable=False)
      
      def __init__(self, title, release_date, movie_id):
          self.title = title
          self.release_date = release_date
          self.movie_id = movie_id

      def insert(self):
          db.session.add(self)
          db.session.commit()

      def update(self):
          db.session.commit()
    
      def delete(self):
          db.session.delete(self)
          db.session.commit()

      def format(self):
          return{
              'id':self.id,
              'title':self.title,
              'release_date':self.release_date
          }

'''
Actor
'''
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    movies = db.relationship('Movie', backref='actor', lazy=True, cascade= 'all , delete')  # parent  

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id':self.id,
            'name':self.name,
            'age':self.age,
            'gender':self.gender
        }