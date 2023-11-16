from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DocumentSerializer
from .tasks import create_document


class DocumentView(APIView):
    """Public API method. Get post request and return Response with a link to document in Google Drive."""

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            valid_data: dict = serializer.validated_data
            document: dict = create_document.delay(valid_data).get()
            return Response(document)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
