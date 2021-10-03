import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


# class TestEmployee:
#     # def test_model(self):
#     #     obj = mixer.blend('payroll.Employee')
#     #     assert obj.pk == 1, 'Should create a Post instance'


# def test_employee():
# 	obj = mixer.blend('payroll.Employee')
# 	result = obj.get_status(5)
# 	assert result == 'Hello', 'Should return first few characters'