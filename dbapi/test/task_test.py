__author__ = 'cody'

from dbapi.test.testing_utils import *

class TaskTest(DbapiTestCase):

    def test_get_task(self):
        return_value = self.app.get("/task/{}".format(self.test_task.id))
        print(return_value)

if __name__ == '__main__':
    unittest.main()
