from datetime import time, timedelta
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from habits.models import Habit


User = get_user_model()


class HabitTestCase(APITestCase):
    """ Habit test case """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email='test@test.com')
        cls.habit = Habit.objects.create(
            name='Test Habit',
            place='Nowhere',
            start_time='04:20:00',
            action='Nothing',
            is_pleasant=False,
            frequency=4,
            reward='Nothing',
            execution_time='00:01:30',
            is_public=True,
            owner=cls.user,
            related_habit=None
        )

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def create_habit(self, **kwargs):
        """ Creates habit with given args (or default) """
        defaults = {
            'name': 'Test Habit',
            'place': 'Nowhere',
            'start_time': '04:20:00',
            'action': 'Nothing',
            'is_pleasant': False,
            'frequency': 4,
            'reward': 'Nothing',
            'execution_time': '00:01:30',
            'is_public': True,
            'owner': self.user,
            'related_habit': None
        }
        defaults.update(kwargs)
        return Habit.objects.create(**defaults)

    def test_habit_create(self):
        url = reverse('habits:habit-list')
        response = self.client.post(url, {
            'name': 'Test habit',
            'place': 'Nowhere',
            'start_time': '04:20:00',
            'action': 'Nothing',
            'is_pleasant': False,
            'frequency': 4,
            'reward': 'Nothing',
            'execution_time': '00:01:30',
            'is_public': True,
            'owner': self.user.id,
            'related_habit': ''
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
        self.assertEqual(Habit.objects.last().name, 'Test habit')
        self.assertEqual(Habit.objects.last().place, 'Nowhere')
        self.assertEqual(Habit.objects.last().start_time, time(4, 20))
        self.assertEqual(Habit.objects.last().action, 'Nothing')
        self.assertEqual(Habit.objects.last().is_pleasant, False)
        self.assertEqual(Habit.objects.last().frequency, 4)
        self.assertEqual(Habit.objects.last().reward, 'Nothing')
        self.assertEqual(Habit.objects.last().execution_time, timedelta(seconds=90))
        self.assertEqual(Habit.objects.last().is_public, True)
        self.assertEqual(Habit.objects.last().owner, self.user)
        self.assertEqual(Habit.objects.last().related_habit, None)

    def test_habit_list(self):
        url = reverse('habits:habit-list')
        habit_1 = self.create_habit(name='Habit 1', place='Place 1')
        habit_2 = self.create_habit(name='Habit 2', place='Place 2')

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['count'], 3)
        self.assertIsNone(data['next'])
        self.assertIsNone(data['previous'])

        expected_results = [
            {
                'id': self.habit.id,
                'name': self.habit.name,
                'place': self.habit.place,
                'start_time': self.habit.start_time,
                'action': self.habit.action,
                'is_pleasant': self.habit.is_pleasant,
                'frequency': self.habit.frequency,
                'reward': self.habit.reward,
                'execution_time': self.habit.execution_time,
                'is_public': self.habit.is_public,
                'owner': self.user.id,
                'related_habit': self.habit.related_habit
            },
            {
                'id': habit_1.id,
                'name': 'Habit 1',
                'place': 'Place 1',
                'start_time': '04:20:00',
                'action': 'Nothing',
                'is_pleasant': False,
                'frequency': 4,
                'reward': 'Nothing',
                'execution_time': '00:01:30',
                'is_public': True,
                'owner': self.user.id,
                'related_habit': None
            },
            {
                'id': habit_2.id,
                'name': 'Habit 2',
                'place': 'Place 2',
                'start_time': '04:20:00',
                'action': 'Nothing',
                'is_pleasant': False,
                'frequency': 4,
                'reward': 'Nothing',
                'execution_time': '00:01:30',
                'is_public': True,
                'owner': self.user.id,
                'related_habit': None
            },
        ]
        self.assertCountEqual(data['results'], expected_results)

    def test_habit_retrieve(self):
        url = reverse('habits:habit-detail', kwargs={'pk': self.habit.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            'id': self.habit.id,
            'name': self.habit.name,
            'place': self.habit.place,
            'start_time': self.habit.start_time,
            'action': self.habit.action,
            'is_pleasant': self.habit.is_pleasant,
            'frequency': self.habit.frequency,
            'reward': self.habit.reward,
            'execution_time': self.habit.execution_time,
            'is_public': self.habit.is_public,
            'owner': self.user.id,
            'related_habit': self.habit.related_habit
        }
        self.assertEqual(response.data, expected_data)

    def test_habit_update(self):
        url = reverse('habits:habit-detail', kwargs={'pk': self.habit.id})
        updated_data = {
            'name': 'Updated Habit',
            'place': 'Somewhere',
            'start_time': '05:30:00',
            'action': 'Something',
            'is_pleasant': False,
            'frequency': 2,
            'reward': 'Something',
            'execution_time': '00:02:00',
            'is_public': False,
            'owner': self.user.id,
            'related_habit': None
        }
        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.name, updated_data['name'])
        self.assertEqual(self.habit.place, updated_data['place'])
        self.assertEqual(self.habit.start_time, time(hour=5, minute=30))
        self.assertEqual(self.habit.action, updated_data['action'])
        self.assertEqual(self.habit.is_pleasant, updated_data['is_pleasant'])
        self.assertEqual(self.habit.frequency, updated_data['frequency'])
        self.assertEqual(self.habit.reward, updated_data['reward'])
        self.assertEqual(self.habit.execution_time, timedelta(seconds=120))
        self.assertEqual(self.habit.is_public, updated_data['is_public'])
        self.assertEqual(self.habit.owner.id, updated_data['owner'])
        self.assertEqual(self.habit.related_habit, updated_data['related_habit'])

    def test_habit_delete(self):
        url = reverse('habits:habit-detail', kwargs={'pk': self.habit.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())
