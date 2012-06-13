from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from mock import Mock

from .models import TestModel, CustomUserFieldNameModel

from ..surgeons import NopSurgeon, DefaultSurgeon

class AppPropertiesTest(TestCase):
    
    def testAppSettingsShouldBePresent(self):
        try:
            settings.TRANSPLANT_OPERATIONS
        except AttributeError:
            self.fail("No TRANSPLANT_OPERATIONS in settings")
        
        try:
            settings.TRANSPLANT_SUCCESS_URL
        except AttributeError:
            self.fail("No TRANSPLANT_SUCCESS_URL")
        
        try:
            settings.TRANSPLANT_FAILURE_URL
        except AttributeError:
            self.fail("No TRANSPLANT_FAILURE_URL")

class NopSurgeonTest(TestCase):
    
    def setUp(self):
        self.receiver = User.objects.create_user(
            username = 'receiver',
            password = 'r'
        )
        self.donor = User.objects.create_user(
            username = 'donor',
            password = 'd'
        )
    
    def testNopSurgeonShouldInitializeProperAttrs(self):
        s = NopSurgeon(TestModel.objects)
        self.assertEquals(s.queryset, TestModel.objects)
    
    def testNopSurgeonShouldBeInitializedWithSomeKwargs(self):
        s1 = NopSurgeon(TestModel.objects)
        self.assertEquals('user', s1.user_field)
        
        s2 = NopSurgeon(TestModel.objects, user_field='owner')
        self.assertEquals('owner', s2.user_field)
    
    def testNopSurgeonShouldImplementMergeMethodThatShouldDoNothing(self):
        s = NopSurgeon(TestModel.objects)
        
        try:
            s.merge(self.receiver, self.donor)
        except AttributeError:
            self.fail("Method merge is not implemented")

class DefaultSurgeonTest(TestCase):
    
    def setUp(self):
        self.receiver = User.objects.create_user(
            username = 'receiver',
            password = 'r'
        )
        self.donor = User.objects.create_user(
            username = 'donor',
            password = 'd'
        )
    
    def testMergeShouldSetDonorInactive(self):
        s = DefaultSurgeon(TestModel.objects)
        s.merge(self.receiver, self.donor)
        self.assertTrue(self.receiver.is_active)
        self.assertFalse(self.donor.is_active)
    
    def testMergeShouldSetUserOnAllObjectsFromQuerysetToReceiver(self):
        for i in range(0,10):
            u = self.receiver if i % 2 == 0 else self.donor
            TestModel(user=u).save()
        s = DefaultSurgeon(TestModel.objects)
        s.merge(self.receiver, self.donor)
        for testmodel in TestModel.objects.all():
            self.assertEquals(self.receiver, testmodel.user)
    
    def testMergeShouldWorkIfUserFieldHasCustomName(self):
        for i in range(0, 10):
            u = self.receiver if i % 2 == 0 else self.donor
            CustomUserFieldNameModel(person=u).save()
        s = DefaultSurgeon(CustomUserFieldNameModel.objects, user_field='person')
        s.merge(self.receiver, self.donor)
        for testmodel in CustomUserFieldNameModel.objects.all():
            self.assertEquals(self.receiver, testmodel.person)
    
    def testMergeShouldCallSaveOnEachObjectInQueryset(self):
        for _ in range(0,10):
            TestModel(user=self.receiver).save()
        mock_list = [Mock(obj) for obj in TestModel.objects.all()]
        TestModel.objects.all = Mock(name='method')
        TestModel.objects.all.return_value = mock_list
        s = DefaultSurgeon(TestModel.objects)
        s.merge(self.receiver, self.donor)
        for mock in mock_list:
            mock.save.assert_called_with()