__author__ = 'cody'

from dbapi.test.testing_utils import *
import json

class TaskTest(DbapiTestCase):

    def test_get_task_success(self):
        return_value = self.app.get("/task/{}".format(self.test_task.id))
        self.assertEqual(self.test_task.todict(), json.loads(return_value.data.decode())["data"])

    def test_get_task_not_found(self):
        return_value = self.app.get("/task/{}".format(666))
        return_text = json.loads(return_value.data.decode())["err"]
        self.assertIn(TASK_NOT_FOUND, return_text)
        self.assertEqual(return_value.status_code, HTTPStatusCodes.NOT_FOUND)

    def test_get_all_tasks(self):
        second_task = self.create_task({"name": "second_task"})
        return_value = self.app.get("/task")
        return_value_data = json.loads(return_value.data.decode())["data"]
        self.assertIn(self.test_task.todict(), return_value_data)
        self.assertIn(second_task.todict(), return_value_data)

    def test_get_all_tasks_none_found(self):
        self.session.delete(self.test_task)
        self.session.commit()
        return_value = self.app.get("/task")
        self.assertEqual(json.loads(return_value.data.decode())["data"], [])

    def test_create_new_task(self):
        new_task_dict = {"name": "new_task"}
        return_value = self.app.post("/task", data=json.dumps(new_task_dict))
        query_result = self.session.query(Task).filter(Task.name == "new_task").first()
        self.assertIsNotNone(query_result)
        self.assertEqual(query_result.name, "new_task")

    def test_create_new_task_already_exists(self):
        query_result = self.session.query(Task).filter(Task.name == self.test_task.name).first()
        self.assertIsNotNone(query_result)
        self.assertEqual(query_result.name, self.test_task.name)

        new_task_dict = {"name": self.test_task.name}
        return_value = self.app.post("/task", data=json.dumps(new_task_dict))
        return_text = json.loads(return_value.data.decode())["err"]
        self.assertEqual(return_text, TASK_ALREADY_EXISTS)
        self.assertEqual(return_value.status_code, HTTPStatusCodes.FORBIDDEN)

    def test_update_task(self):
        update_task_dict = {"name": self.test_task.name, "desc": "updated_desc"}
        return_value = self.app.post("/task/{}".format(self.test_task.id), data=json.dumps(update_task_dict))
        self.session.expire_all()
        query_result = self.session.query(Task).filter(Task.name == self.test_task.name).scalar()
        self.assertEqual(query_result.desc, "updated_desc")

    def test_update_task_not_found(self):
        update_task_dict = {"name": self.test_task.name, "desc": "updated_desc"}
        return_value = self.app.post("/task/{}".format(666), data=json.dumps(update_task_dict))
        return_text = json.loads(return_value.data.decode())["err"]
        self.assertIn(TASK_NOT_FOUND, return_text)
        self.assertEqual(return_value.status_code, HTTPStatusCodes.NOT_FOUND)

    def test_delete_task(self):
        return_value = self.app.delete("/task/{}".format(self.test_task.id))
        query_result = self.session.query(Task).filter(Task.id == self.test_task.id).first()
        self.assertIsNone(query_result)

    def test_delete_task_not_found(self):
        return_value = self.app.delete("/task/{}".format(666))
        return_text = json.loads(return_value.data.decode())["err"]
        self.assertIn(TASK_NOT_FOUND, return_text)
        self.assertEqual(return_value.status_code, HTTPStatusCodes.NOT_FOUND)

    def test_complete_task(self):
        return_value = self.app.post("/task/{}/finish".format(self.test_task.id))
        self.session.expire_all()
        query_result = self.session.query(Task).filter(Task.id == self.test_task.id).scalar()
        self.assertIsNotNone(query_result.end)

    def test_complete_task_not_found(self):
        return_value = self.app.post("/task/{}/finish".format(666))
        return_text = json.loads(return_value.data.decode())["err"]
        self.assertIn(TASK_NOT_FOUND, return_text)
        self.assertEqual(return_value.status_code, HTTPStatusCodes.NOT_FOUND)
        
if __name__ == '__main__':
    unittest.main()
