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




if __name__ == '__main__':
    unittest.main()
