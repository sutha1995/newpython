
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv() # Load environment variables from .env file

mongo_uri = os.getenv('MONGODB_AATLAS_CLUSTER_URI') # Get MongoDB URI from environment variable

class DatabaseManager:
    def __init__(self, db_name='example_db', connection_string=mongo_uri):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.users_collection = self.db.users
        self.posts_collection = self.db.posts
        self.init_database()

    def init_database(self):
        """Initialize database with collections and indexes"""
        # Create unique index on email for users
        self.users_collection.create_index('email', unique=True)
        # Create index on author_id for posts for better query performance
        self.posts_collection.create_index("user_id")

    def create_user(self, name, email, age):
        """Create a new user"""
        try:
            user_doc = {
                "name": name,
                "email": email,
                "age": age,
                "created_at": datetime.now()
            }
            result = self.users_collection.insert_one(user_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error: {e}")
            return None
        
    def create_post(self, user_id, title, content):
        """Create a new post"""
        try:
            # Convert string user_id to ObjectId if it's a valid ObjectId
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id
            
            post_doc = {
                "user_id": ObjectId(user_id),
                "title": title,
                "content": content,
                "created_at": datetime.now()
            }
            result = self.posts_collection.insert_one(post_doc)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating post: {e}")
            return None
        
    def get_all_users(self):
        """Get all users"""
        try:
            users = list(self.users_collection.find())
            #Convert ObjectId to string for display
            for user in users:
                user['_id'] = str(user['_id'])  # Convert ObjectId to string for easier handling
            return users
        except Exception as e:
            print(f"Error retrieving users: {e}")
            return []
        
    def get_user_by_id(self, user_id):
        """Get posts by user"""
        try:
            # Convert string user_id to ObjectId if it's a valid ObjectId
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id
            
            posts = list(self.posts_collection.find(
                {"user_id": user_object_id}
                ).sort("created_at", -1))
            
            # Convert ObjectId to string for display
            for post in posts:
                post['_id'] = str(post['_id'])
                post['user_id'] = str(post['user_id'])
            
            return posts
        except Exception as e:
            print(f"Error fetching posts: {e}")
            return []
        
    def delete_user(self, user_id):
        """Delete a user and their posts"""
        try:
            # Convert string user_id to ObjectId if it's a valid ObjectId
            if ObjectId.is_valid(user_id):
                user_object_id = ObjectId(user_id)
            else:
                user_object_id = user_id
            
            # Delete user's post first
            self.posts_collection.delete_many({"user_id": user_object_id})

            # Delete the user
            result = self.users_collection.delete_one({"_id": user_object_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
        
    def class_connection(self):
        """Close the FastAPI connection"""
        self.client.close()
