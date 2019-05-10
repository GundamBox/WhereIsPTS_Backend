import random
import string
import time
import unittest
from sqlalchemy import text
from flask_migrate import Migrate

from os import path
import sys

sys.path.append(path.abspath(path.join(path.dirname(__file__), '../../')))


from app import create_app, db


class WhereIsPTSApiTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.store = []
        cls.app = create_app('testing')

        db.init_app(cls.app)

        cls.db = db
        cls.db.drop_all()
        cls.db.create_all()

        sql = text('''
INSERT INTO channel(id, name)
VALUES (1,'公視新聞'),
    (2,'TVBS新聞'),
    (3,'中天新聞'),
    (4,'民視新聞'),
    (5,'中視新聞'),
    (6,'華視新聞'),
    (7,'三立新聞'),
    (8,'東森新聞'),
    (9,'年代新聞'),
    (10,'非凡新聞'),
    (11,'壹電視新聞'),
    (12,'體育新聞'),
    (13,'不是新聞');''')
        result = db.engine.execute(sql)

    def setUp(self):
        self._started_at = time.time()

    def tearDown(self):
        elapsed = time.time() - self._started_at
        print('{} ({}s)'.format(self.id(), round(elapsed, 2)))

    def test_store_create(self):
        with self.app.test_client() as client:
            resp = client.post('/api/v1/store', data={
                'name': '和春麵館',
                'lat': 22.980661,
                'lng': 120.217050,
                'address': '台南市東區崇明路73號',
                'switchable': 'false'
            })
            self.assertEqual(resp.status_code, 201)

            store_json = resp.get_json()
            store_id = store_json['sid']
            self.assertEqual(store_id, 1)

        with self.app.test_client() as client:
            resp = client.post('/api/v1/store', data={
                'name': '李師傅牛肉拉麵',
                'lat': 22.612640,
                'lng': 120.344372,
                'address': '高雄市鳳山區新康街300號',
                'switchable': 'false'
            })
            store_json = resp.get_json()
            store_id = store_json['sid']
            self.assertEqual(resp.status_code, 201)
            self.assertEqual(store_id, 2)

    def test_store_read(self):
        with self.app.test_client() as client:
            resp = client.get('/api/v1/store/1')
            store_json = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(store_json['sid'], 1)
            self.assertEqual(store_json['name'], '和春麵館')
            self.assertAlmostEqual(
                store_json['location'][0], 22.980661, places=6)
            self.assertAlmostEqual(
                store_json['location'][1], 120.217050, places=6)
            self.assertEqual(store_json['address'], '台南市東區崇明路73號')
            self.assertFalse(store_json['switchable'])

        with self.app.test_client() as client:
            resp = client.get('/api/v1/store/2')
            store_json = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(store_json['sid'], 2)
            self.assertEqual(store_json['name'], '李師傅牛肉拉麵')
            self.assertAlmostEqual(
                store_json['location'][0], 22.612640, places=6)
            self.assertAlmostEqual(
                store_json['location'][1], 120.344372, places=6)
            self.assertEqual(store_json['address'], '高雄市鳳山區新康街300號')
            self.assertFalse(store_json['switchable'])

    def test_store_read_list(self):
        with self.app.test_client() as client:
            resp = client.get(
                '/api/v1/store/list?lat=22.982320&lng=120.215007')
            self.assertEqual(resp.status_code, 200)
            result_json = resp.get_json()

            store_list_json = result_json['result']
            store0 = store_list_json[0]
            self.assertEqual(store0['sid'], 1)
            self.assertEqual(store0['name'], '和春麵館')
            self.assertAlmostEqual(store0['location'][0], 22.980661, places=6)
            self.assertAlmostEqual(store0['location'][1], 120.217050, places=6)
            self.assertEqual(store0['address'], '台南市東區崇明路73號')
            self.assertFalse(store0['switchable'])

            count = result_json['total']
            self.assertEqual(count, 1)

    def test_store_update(self):
        with self.app.test_client() as client:
            resp = client.put('/api/v1/store/2', data={
                'switchable': 'true'
            })
            self.assertEqual(resp.status_code, 201)

            store_json = resp.get_json()

            self.assertEqual(store_json['sid'], 2)
            self.assertEqual(store_json['name'], '李師傅牛肉拉麵')
            self.assertAlmostEqual(
                store_json['location'][0], 22.612640, places=6)
            self.assertAlmostEqual(
                store_json['location'][1], 120.344372, places=6)
            self.assertEqual(store_json['address'], '高雄市鳳山區新康街300號')
            self.assertTrue(store_json['switchable'])

    def test_store_delete(self):
        with self.app.test_client() as client:
            resp = client.delete('/api/v1/store/1')
            self.assertEqual(resp.status_code, 204)

        with self.app.test_client() as client:
            resp = client.get('/api/v1/store/1')
            store_json = resp.get_json()
            self.assertEqual(resp.status_code, 404)

    def test_vote_store(self):

        for _ in range(2):
            with self.app.test_client() as client:
                resp = client.post('/api/v1/vote/store/2', data={
                    'cid': 1
                })

        with self.app.test_client() as client:
            resp = client.post('/api/v1/vote/store/2', data={
                'cid': 2
            })

        with self.app.test_client() as client:
            resp = client.get('/api/v1/store/2')
            store_json = resp.get_json()
            votes = store_json['votes']

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(votes[0]['vote_count'], 2)
            self.assertEqual(votes[1]['vote_count'], 1)

    def test_channel_create(self):
        pass

    def test_channel_read(self):
        pass

    def test_channel_read_list(self):
        pass

    def test_channel_update(self):
        pass

    def test_channel_delete(self):
        pass

if __name__ == '__main__':
    unittest.main()
