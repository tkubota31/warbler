"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        user1 = User.signup("test1", "email1@email.com", "password", None)
        uid1 = 1111
        user1.id = uid1

        user2 = User.signup("test2", "email2@email.com", "password", None)
        uid2 = 2222
        user2.id = uid2

        db.session.commit()

        user1 = User.query.get(uid1)
        user2 = User.query.get(uid2)

        self.u1ser = user1
        self.uid1 = uid1

        self.user2 = user2
        self.uid2 = uid2

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)


    # def test_user_follow(self):
    #     self.user1.following.append(self.user2)
    #     db.session.commit()

    #     self.assertEqual(len(self.user2.following),0)
    #     self.assertEqual(len(self.user1.following),1)

    def test_is_following(self):
        self.user1.following.appened(self.user2)
        db.session.commit()

        self.assertTrue(self.user1.is_following(self.user2))
        self.assertFalse(self.user2.is_following(self.user1))

    def test_is_followed_by(self):
        self.user1.following.appened(self.user2)
        db.session.commit()

        self.assertTrue(self.user2.is_followed_by(self.user1))
        self.assertFalse(self.user1.is_followed_by(self.user2))

    def test_user_signup(self):
        user_test = User.signup("taioh","password","email@gmail.com",None)
        userid = 1234
        user_test.id = userid
        db.session.commit()
        user_test = User.query.get_or_404(userid)
        self.assertEqual(user_test.username,"taioh")
        self.assertEqual(user_test.password,"password")
        self.assertEqual(user_test.email,"email@gmail.com")

    def test_user_fail(self):
        user_test = User.signup("taioh", None, None)
        userid = 3
        user_test.id = userid
        db.session.commit()
        self.assertEqual(User.query.get_or_404(userid), 404)

    def test_user_authenticate(self):
        self.assertFalse(self.user1.authenticate("test1","emailunch@email.com"))
        self.assertFalse(self.user1.authenticate("testtt1","email1@email.com"))
        self.assertEqual(self.user1.authenticate("test1","email1@email.com"),self.user1)
