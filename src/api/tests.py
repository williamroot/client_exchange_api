# from django.core.urlresolvers import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from rest_framework.test import force_authenticate
# from django.contrib.auth.models import User

# class AccountTests(APITestCase):
#     def test_fail_create_account(self):
#         """
#         Ensure can't create user without auth
#         """
#         url = '/api/users'
#         data = {'name': 'william'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(
#             response.status_code, status.HTTP_301_MOVED_PERMANENTLY
#         )

#     def test_create_account(self):
#         """
#         Ensure can't create user without auth
#         """
#         url = '/api/users'
#         data = {'name': 'william'}
#         import pdb;pdb.set_trace()
#         user = User.objects.get(username='william')

#         force_authenticate(request, user=user)
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(
#             response.status_code, status.HTTP_301_MOVED_PERMANENTLY
#         )

