# services/users/project/tests/test_user_model.py


import unittest

from sqlalchemy.exc import IntegrityError

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user


class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user('alex', 'alex@gmail.com')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'alex')
        self.assertEqual(user.email, 'alex@gmail.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        add_user('alex', 'alex@gmail.com')
        duplicate_user = User(
            username='alex',
            email='ender@gmail.com',
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        add_user('alex', 'alex@gmail.com')
        duplicate_user = User(
            username='ender',
            email='alex@gmail.com',
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_to_json(self):
        user = add_user('alex', 'alex@gmail.com')
        self.assertTrue(isinstance(user.to_json(), dict))


if __name__ == '__main__':
    unittest.main()
