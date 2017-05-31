import subprocess
import tempfile
import os

from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APISimpleTestCase

from app.tasks import download_file_from_url, calculate_md5sum
from web.settings import BASE_DIR
from app.tasks import app


class CeleryTasksTestCase(SimpleTestCase):

    def test_calculate_md5sum(self):
        pathname = "Dockerfile"
        result = str(calculate_md5sum(pathname))
        cmd_result = subprocess.run(["md5sum", pathname],
                                    stdout=subprocess.PIPE)
        self.assertEqual(result, cmd_result.stdout.split()[0].decode("utf-8"))

    def test_download_file_local(self):
        location = "Dockerfile"
        f, pathname = tempfile.mkstemp()
        os.close(f)
        download_file_from_url("file://" + BASE_DIR +
                               "/" + location, pathname)
        self.assertEqual(os.stat(location).st_size, os.stat(pathname).st_size)

    def test_download_file_from_url(self):
        f, pathname = tempfile.mkstemp()
        os.close(f)
        download_file_from_url("http://example.com", pathname)
        self.assertTrue(os.stat(pathname).st_size > 0)


class AppAPITestCase(APISimpleTestCase):

    def test_post_request(self):
        response = self.client.post("/", "http://example.com".encode("utf-8"),
                                    content_type="text/plain")
        self.assertTrue(len(response.data) > 0)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_get_wrong_guid(self):
        response = self.client.get("/wrong-guid/")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_integrated_correct_url(self):
        response_post = self.client.post("/",
                                         "http://example.com".encode("utf-8"),
                                         content_type="text/plain")
        self.assertTrue(len(response_post.data) > 0)
        self.assertEqual(response_post.status_code, status.HTTP_202_ACCEPTED)

        task = app.AsyncResult(response_post.data)
        task.wait(timeout=10)
        task = task.children[0]
        task.wait(timeout=10)

        response_get = self.client.get("/" + response_post.data + "/")
        self.assertEqual(response_get.status_code, status.HTTP_200_OK,
                         msg="This test may fail if URL in POST request is \
                         unreachable or execution time is over (20sec/test)")
        self.assertTrue(len(response_get.data) == 32)

    def test_integrated_incorrect_url(self):
        response_post = self.client.post("/",
                                         "wrong-url".encode("utf-8"),
                                         content_type="text/plain")
        self.assertTrue(len(response_post.data) > 0)
        self.assertEqual(response_post.status_code, status.HTTP_202_ACCEPTED)

        try:
            task = app.AsyncResult(response_post.data)
            task.wait(timeout=10)
        except:
            pass

        response_get = self.client.get("/" + response_post.data + "/")
        self.assertEqual(response_get.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(len(response_get.data) > 0)
