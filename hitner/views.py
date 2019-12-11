from hitner.utils import HLT
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response


class NerView(APIView):
    def post(self, request):
        result = {'status': 1, 'msg': None, 'data': None}
        data = request.POST.dict()
        ner = HLT(settings.MODEL_PATH).start(data['txt'])
        result['data'] = ner
        return Response(result)
