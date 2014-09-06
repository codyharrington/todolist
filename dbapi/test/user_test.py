__author__ = 'cody'

from dbapi.test.testing_utils import *
import json

class UserTest(DbapiTestCase):

    def test_get_user_success(self):
        return_value = self.app.get("/user/{}".format(self.test_user.username))
        self.assertEqual(self.test_user.todict(), json.loads(return_value.data.decode())["data"])

    def test_get_user_not_found(self):
        return_value = self.app.get("/user/{}".format(666))
        return_text = json.loads(return_value.data.decode())["err"]
        self.assertIn(USER_NOT_FOUND, return_text)
        self.assertEqual(return_value.status_code, HTTPStatusCodes.NOT_FOUND)

    def test_get_all_users(self):
        second_user = self.create_user({"username": "second_user", "password": "password"})
        return_value = self.app.get("/user")
        return_value_data = json.loads(return_value.data.decode())["data"]
        self.assertIn(self.test_user.todict(), return_value_data)
        self.assertIn(second_user.todict(), return_value_data)

    def test_get_all_users_none_found(self):
        self.session.delete(self.test_user)
        self.session.commit()
        return_value = self.app.get("/user")
        self.assertEqual(json.loads(return_value.data.decode())["data"], [])

    def test_create_new_user(self):
        new_user_dict = {"username": "new_user", "password": "password"}
        return_value = self.app.post("/user", data=json.dumps(new_user_dict))
        query_result = self.session.query(User).filter(User.username == "new_user").first()
        self.assertIsNotNone(query_result)
        self.assertEqual(query_result.username, "new_user")

    def test_create_new_user_already_exists(self):
        query_result = self.session.query(User).filter(User.username == self.test_user.username).first()
        self.assertIsNotNone(query_result)
        self.assertEqual(query_result.username, self.test_user.username)

        new_user_dict = {"username": self.test_user.username, "password": "foopassword"}
        return_value = self.app.post("/user", data=json.dumps(new_user_dict))
        return_text = json.loads(return_value.data.decode())["err"]
        self.assertEqual(return_text, USER_ALREADY_EXISTS)
        self.assertEqual(return_value.status_code, HTTPStatusCodes.FORBIDDEN)

    def test_update_user(self):
        update_user_dict = {"username": self.test_user.username, "email": "updated_email"}
        return_value = self.app.post("/user/{}".format(self.test_user.username), data=json.dumps(update_user_dict))
        self.session.expire_all()
        query_result = self.session.query(User).filter(User.username == self.test_user.username).scalar()
        self.assertEqual("updated_email", query_result.email)

    def test_update_user_not_found(self):
        update_user_dict = {"name": self.test_user.username, "email": "updated_email"}
        return_value = self.app.post("/user/{}".format(666), data=json.dumps(update_user_dict))
        return_text = json.loads(return_value.data.decode())["err"]
        self.assertIn(USER_NOT_FOUND, return_text)
        self.assertEqual(return_value.status_code, HTTPStatusCodes.NOT_FOUND)

    def test_delete_user(self):
        return_value = self.app.delete("/user/{}".format(self.test_user.username))
        query_result = self.session.query(User).filter(User.id == self.test_user.username).first()
        self.assertIsNone(query_result)

    def test_delete_user_not_found(self):
        return_value = self.app.delete("/user/{}".format(666))
        return_text = json.loads(return_value.data.decode())["err"]
        self.assertIn(USER_NOT_FOUND, return_text)
        self.assertEqual(return_value.status_code, HTTPStatusCodes.NOT_FOUND)

    def test_authenticate_user_success(self):
        auth_dict = {"username": self.test_user.username, "password": self.test_user.password}
        return_value = self.app.post("/user/authenticate", data=json.dumps(auth_dict))
        self.assertEqual(self.test_user.todict(), json.loads(return_value.data.decode())["data"])

if __name__ == '__main__':
    unittest.main()
