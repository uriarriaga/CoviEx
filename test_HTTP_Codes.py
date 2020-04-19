from app import app
import unittest


class MainTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/",content_type="html/text")
        self.assertEqual(response.status_code, 302)
    
    def test_login (self):
        tester = app.test_client(self)
        response = tester.get("/login",content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_democonstula (self):
        tester = app.test_client(self)
        response = tester.get("/democonstula",content_type="html/text")
        self.assertEqual(response.status_code, 200)
    
    def test_repuestateleconsulta(self):
        tester = app.test_client(self)
        response = tester.get("/repuestateleconsulta",content_type="html/text")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()