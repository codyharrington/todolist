__author__ = 'cody'

from dbapi.test.testing_utils import *
import json

class TaskTest(DbapiTestCase):

    def test_get_task(self):
        return_value = self.app.get("/task/{}".format(self.test_task.id))
        self.assertEqual(self.test_task.todict(), json.loads(return_value.data.decode())["data"])


if __name__ == '__main__':
    unittest.main()
