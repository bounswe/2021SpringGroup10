import unittest
import xmlrunner
from HtmlTestRunner import HTMLTestRunner
import os
import main

class Test(unittest.TestCase):

    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()
        self.mock_data_1 = [
            {"fname": "ali", "lname": "veli", "message": "good job! looking good already."},
            {"fname": "ayşe", "lname": "fatma", "message": "hey guys why did you kick me out of the group??"},
            {"fname": "murat", "lname": "sürat", "message": "I was wondering if you guys need help with anything."}
        ]
        self.mock_data_2 = [
            "60be86c17feaf4a3ec8cc2f7",
            "60be86e37feaf4a3ec8cc2f8",
            "60be869d24a8c2ba5c5d1f9a"
        ]

    def test_write2channel(self):
        for data in self.mock_data_1:
            return_value = self.app.post(f'/write2channel/{data["fname"]}/{data["lname"]}/{data["message"]}')
            self.assertEqual(return_value.status, '200 OK')
    
    def test_check_replies(self):
        for data in self.mock_data_2:
            return_value = self.app.get(f'/slack-replies/{data}')
            self.assertEqual(return_value.status, '200 OK')

if __name__ == '__main__':
    # create a runner to see the output test reports
    root_dir = os.path.dirname(__file__)
    test_loader = unittest.TestLoader()
    package_tests = test_loader.discover(start_dir=root_dir)

    runner = xmlrunner.XMLTestRunner(output='./reports/xml/')

    # XML runner -- can be useful for automated testing

    runner = xmlrunner.XMLTestRunner(output='./reports/xml/')
    runner = HTMLTestRunner(combine_reports=True, report_name="MyReport", add_timestamp=False)

    # To run the HTML runner for nice reports uncomment the following

    #  runner = HTMLTestRunner(combine_reports=True, report_name="MyReport", add_timestamp=False)
    runner = HTMLTestRunner(combine_reports=True, output='./reports/html/', report_name="Write2Us-Tests-Report", add_timestamp=True)

    unittest.main(testRunner=runner)
