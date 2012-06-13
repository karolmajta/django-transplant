from django.test import TestCase
from django.conf import settings

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
    
    def testNopSurgeonShouldBeInitialisedWithKwargs(self):
        pass