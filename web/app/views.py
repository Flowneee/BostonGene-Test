# coding: utf-8

import tempfile
import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from .tasks import download_file_from_url, calculate_md5sum
from web.celery import app


def nice_traceback(traceback, guid):
    ret = ["Whoops! Error occured in task " + guid, ""]
    ret += traceback.split("\n")
    return ret


class Md5HashViewSet(viewsets.ViewSet):

    def create(self, request):
        f, pathname = tempfile.mkstemp()
        os.close(f)
        task = download_file_from_url.s(request.data.decode("utf-8"), pathname)
        task.link(calculate_md5sum.s())
        ares = task.delay()
        return Response(ares.id, status=status.HTTP_202_ACCEPTED)

    def retrieve(self, request, pk=None):
        task = app.AsyncResult(pk)
        if task.successful() and task.children[0].successful():
            return Response(task.children[0].result, status=status.HTTP_200_OK)
        else:
            if task.failed():
                return Response(nice_traceback(task.traceback, pk),
                                status=status.HTTP_400_BAD_REQUEST)
            if task.children is not None:
                if task.children[0].failed():
                    return Response(nice_traceback(task.children[0].traceback,
                                                   task.children[0].id),
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_409_CONFLICT)
