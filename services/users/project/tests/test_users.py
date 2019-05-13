# services/users/project/tests/test_users.py

from project import db
from project.api.models import User

import json
import unittest

from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""
    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Asegurando que un nuevo usuario pueda ser agregado a la base de
        datos."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'alex',
                    'email': 'alexsanchez@upeu.edu.pe'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn(
                    'alexsanchez@upeu.edu.pe ha sido agregado!',
                    data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Asegurando de que se produce un error si el objeto JSON está
        vacío."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({}),
                content_type='application/json',
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga invalida.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """Asegurando de que se produce un error si el objeto JSON no tiene
        una clave de nombre de usuario.
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'alexsanchez@upeu.edu.pe'}),
                content_type='application/json',
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga invalida.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Asegúrate de que se produce un error si el correo electrónico ya
        existe."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'alex',
                    'email': 'alexsanchez@upeu.edu.pe'
                    }),
                content_type='application/json',
                )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'alex',
                    'email': 'alexsanchez@upeu.edu.pe'
                    }),
                content_type='application/json',
                )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Asegurando de que el usuario individual se comporte
        correctamente."""
        user = add_user('alex', 'alexsanchez@upeu.edu.pe')
        with self.client:
            response = self.client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('alex', data['data']['username'])
            self.assertIn('alexsanchez@upeu.edu.pe', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Asegurando de que se arroje un error si no se proporciona
        una identificación."""
        with self.client:
            response = self.client.get('/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Asegurando de que se arroje un error si la identificación
        no existe."""
        with self.client:
            response = self.client.get('/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Asegurando de que todos los usuarios se comporten correctamente."""
        add_user('alex', 'alexsanchez@upeu.edu.pe')
        add_user('ender', 'endersanchez@upeu.edu.pe')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn('alex', data['data']['users'][0]['username'])
            self.assertIn(
                'alexsanchez@upeu.edu.pe', data['data']['users'][0]['email'])
            self.assertIn('ender', data['data']['users'][1]['username'])
            self.assertIn(
                'endersanchez@upeu.edu.pe', data['data']['users'][1]['email'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """Asegurando de que la ruta
        principal se comporte
        correctamente cuando no se haya agregado ningún usuario a la
        base de datos."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Todos los usuarios', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_with_users(self):
        """Asegúrese de que la ruta principal se
        comporta correctamente cuando los usuarios han sido
        añadido a la base de datos."""
        add_user('alex', 'alexsanchez@upeu.edu.pe')
        add_user('ender', 'endersanchez@upeu.edu.pe')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los usuarios', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'alex', response.data)
            self.assertIn(b'ender', response.data)

    def test_main_add_user(self):
        """Ensure a new user can be
        added to the database via a POST request."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='alex', email='alexsanchez@upeu.edu.pe'),
                follow_redirects=True
                )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los usuarios', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'alex', response.data)

    if __name__ == '__main__':
        unittest.main()
