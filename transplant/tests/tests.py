from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

from .models import TestModel

from ..surgeons import NopSurgeon

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
        s = NopSurgeon(self.receiver, self.donor, TestModel)
        self.assertEquals(s.donor, self.donor)
        self.assertEquals(s.receiver, self.receiver)
        self.assertEquals(s.model, TestModel)
    
    def testNopSurgeonShouldBeInitializedWithSomeKwargs(self):
        s = NopSurgeon(self.receiver, self.donor, TestModel)
        self.assertEquals('user', s.user_field)
        self.assertEquals('objects', s.queryset)