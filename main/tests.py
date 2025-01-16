from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from main.models import RefBook, RefBookVersion, RefBookElement
from django.utils import timezone
from datetime import timedelta


class RefBookTests(TestCase):
    def setUp(self):
        self.refbook = RefBook.objects.create(
            code="refbook_001", name="Справочник 1", description="Описание справочника"
        )
        self.version_1 = RefBookVersion.objects.create(
            refbook=self.refbook, version="1.0", start_date=timezone.now() - timedelta(days=1)
        )
        self.version_2 = RefBookVersion.objects.create(
            refbook=self.refbook, version="2.0", start_date=timezone.now()
        )
        self.element_1 = RefBookElement.objects.create(
            version=self.version_1, code="code1", value="value1"
        )
        self.element_2 = RefBookElement.objects.create(
            version=self.version_2, code="code2", value="value2"
        )

        self.client = APIClient()

    def test_get_refbooks(self):
        """Тестируем получение списка всех справочников"""
        response = self.client.get('/api/refbooks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['refbooks'][0]['name'], 'Справочник 1')

    def test_get_refbooks_with_date_filter(self):
        """Тестируем фильтрацию справочников по дате начала версии"""
        response = self.client.get('/api/refbooks/', {'date': timezone.now().date().strftime('%Y-%m-%d')})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['refbooks'][0]['name'], 'Справочник 1')

    def test_get_refbook_elements(self):
        """Тестируем получение элементов справочника по ID"""
        response = self.client.get(f'/api/refbooks/{self.refbook.id}/elements/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['elements']), 1)

    def test_get_refbook_elements_with_version(self):
        """Тестируем получение элементов для конкретной версии"""
        response = self.client.get(
            f'/api/refbooks/{self.refbook.id}/elements/', {'version': '1.0'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['elements']), 1)
        self.assertEqual(response.data['elements'][0]['code'], 'code1')

    def test_get_refbook_elements_not_found(self):
        """Тестируем случай, когда версия справочника не найдена"""
        response = self.client.get(
            f'/api/refbooks/{self.refbook.id}/elements/', {'version': '3.0'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_check_element_valid(self):
        """Тестируем проверку существования элемента"""
        response = self.client.get(
            f'/api/refbooks/{self.refbook.id}/check_element/', {'code': 'code1', 'value': 'value1'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['valid'], True)

    def test_check_element_invalid(self):
        """Тестируем проверку элемента, которого нет в базе"""
        response = self.client.get(
            f'/api/refbooks/{self.refbook.id}/check_element/', {'code': 'code3', 'value': 'value3'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['valid'], False)

    def test_check_element_missing_params(self):
        """Тестируем случай, когда не переданы обязательные параметры 'code' и 'value'"""
        response = self.client.get(f'/api/refbooks/{self.refbook.id}/check_element/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Parameters code and value must be provided", str(response.content))

    def test_check_element_version(self):
        """Тестируем проверку элемента для конкретной версии"""
        response = self.client.get(
            f'/api/refbooks/{self.refbook.id}/check_element/', {'code': 'code1', 'value': 'value1', 'version': '1.0'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['valid'], True)

    def test_check_element_version_not_found(self):
        """Тестируем проверку элемента для версии, которой нет в базе"""
        response = self.client.get(
            f'/api/refbooks/{self.refbook.id}/check_element/', {'code': 'code1', 'value': 'value1', 'version': '3.0'}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


