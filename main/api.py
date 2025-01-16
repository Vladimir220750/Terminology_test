from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from main.models import RefBook, RefBookVersion
from main.serializers import RefBookElementSerializer, RefBookSerializer


class RefBookListView(APIView):
    @swagger_auto_schema(
        operation_description="Получить список всех справочников.",
        responses={200: RefBookSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('date', openapi.IN_QUERY,
                              description="Фильтрация по дате начала версии справочника.",
                              type=openapi.TYPE_STRING),
        ],
        tags=['Справочники']
    )
    def get(self, request, *args, **kwargs):
        date = request.query_params.get('date')
        if date:
            refbooks = RefBook.objects.filter(versions__start_date__lte=date).distinct()
        else:
            refbooks = RefBook.objects.all()
        serializer = RefBookSerializer(refbooks, many=True)
        return Response({"refbooks": serializer.data})


class RefBookElementListView(APIView):
    @swagger_auto_schema(
        operation_description="Получить список элементов справочника по его ID.",
        responses={200: RefBookElementSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('version', openapi.IN_QUERY,
                              description="Версия справочника, по которой будут выведены элементы.",
                              type=openapi.TYPE_STRING),
        ],
        tags=['Элементы']
    )
    def get(self, request, id):
        version_param = request.query_params.get('version')
        refbook = get_object_or_404(RefBook, id=id)

        try:
            if version_param:
                version = get_object_or_404(RefBookVersion, refbook=refbook, version=version_param)
            else:
                version = refbook.versions.filter(start_date__lte=now().date()).latest('start_date')
        except RefBookVersion.DoesNotExist:
            return Response(
                {"detail": "Reference book version that satisfies the request was not found"},
                status=404
            )

        elements = version.elements.all()
        if not elements:
            return Response({"detail": "Reference book elements not found"}, status=404)

        serializer = RefBookElementSerializer(elements, many=True)
        return Response({"elements": serializer.data})


class CheckElementView(APIView):
    @swagger_auto_schema(
        operation_description="Проверить, существует ли элемент с указанным кодом и значением в справочнике.",
        responses={200: openapi.Response('Ответ с результатом проверки',
                                         schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                         'valid': openapi.Schema(type=openapi.TYPE_BOOLEAN)
        }))},
        manual_parameters=[
            openapi.Parameter('code', openapi.IN_QUERY,
                              description="Код элемента.", type=openapi.TYPE_STRING),
            openapi.Parameter('value', openapi.IN_QUERY,
                              description="Значение элемента.", type=openapi.TYPE_STRING),
            openapi.Parameter('version', openapi.IN_QUERY,
                              description="Версия справочника для проверки.", type=openapi.TYPE_STRING),
        ],
        tags=['Проверка элемента']
    )
    def get(self, request, id):
        code = request.query_params.get('code')
        value = request.query_params.get('value')
        version_param = request.query_params.get('version')

        if not code or not value:
            return Response(
                {"detail": "Parameters code and value must be provided"},
                status=400
            )

        refbook = get_object_or_404(RefBook, id=id)

        try:
            if version_param:
                version = get_object_or_404(RefBookVersion, refbook=refbook, version=version_param)
            else:
                version = refbook.versions.filter(start_date__lte=now().date()).latest('start_date')
        except RefBookVersion.DoesNotExist:
            return Response(
                {"detail": "Reference book version that satisfies the request was not found"},
                status=404
            )

        exists = version.elements.filter(code=code, value=value).exists()

        return Response({"valid": exists})
