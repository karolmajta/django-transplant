from django.test import TestCase, TransactionTestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.core.exceptions import ImproperlyConfigured
from mock import Mock

from .models import TestModel, CustomUserFieldNameModel
from ..surgeons import NopSurgeon, DefaultSurgeon, BatchSurgeon
from ..surgery import Surgery
from ..views import TransplantMergeView

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
        self.assertEquals(s.manager, TestModel.objects)
    
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
    
    def testMergeShouldSetUserOnAllObjectsFromManagerToReceiver(self):
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
    
    def testMergeShouldNotTouchOtherUsersObjects(self):
        stranger = User.objects.create_user(username='s', password='p')
        for i in range(0,10):
            u = self.receiver if i % 2 == 0 else self.donor
            TestModel(user=u).save()
        for _ in range(0,5):
            TestModel(user=stranger).save()
        s = DefaultSurgeon(TestModel.objects)
        s.merge(self.receiver, self.donor)
        self.assertEquals(5, TestModel.objects.filter(user=stranger).count())
    
    def testSameAccountMergeDoesNotDeactivateTheUser(self):
        s = DefaultSurgeon(TestModel.objects)
        s.merge(self.receiver, self.receiver)
        self.assertTrue(self.receiver.is_active)
        
    def testMergeShouldCallSaveOnEachMatchingObjectInManager(self):
        for _ in range(0,10):
            TestModel(user=self.donor).save()
        s = DefaultSurgeon(TestModel.objects)
        s.merge(self.receiver, self.donor)
        for m in TestModel.objects.all():
            self.assertTrue(m.was_saved)

class BatchSurgeonTest(TestCase):
    
    def setUp(self):
        self.receiver = User.objects.create_user(
            username = 'receiver',
            password = 'r'
        )
        self.donor = User.objects.create_user(
            username = 'donor',
            password = 'd'
        )
    
    def testSameAccountMergeDoesNotDeactivateTheUser(self):
        s = DefaultSurgeon(TestModel.objects)
        s.merge(self.receiver, self.receiver)
        self.assertTrue(self.receiver.is_active)
    
    def testMergeShoulNotCallSaveOnEachMatchingObjectInManager(self):
        for _ in range(0,10):
            TestModel(user=self.donor).save()
        s = BatchSurgeon(TestModel.objects)
        s.merge(self.receiver, self.donor)
        for m in TestModel.objects.all():
            self.assertFalse(m.was_saved)
    
    def testMergeShouldSetDonorInactive(self):
        s = DefaultSurgeon(TestModel.objects)
        s.merge(self.receiver, self.donor)
        self.assertTrue(self.receiver.is_active)
        self.assertFalse(self.donor.is_active)
    
    def testMergeShouldSetUserOnAllObjectsFromManagerToReceiver(self):
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

class SurgeryTest(TestCase):

    def testSplitPathShouldReturnTupleWithModuleAndClassname(self):
        surgery = Surgery(
          'transplant.tests.models.TestModel',
          'transplant.surgeons.NopSurgeon'
        )
        result = surgery.split_path('module.path.ClassName')
        self.assertEquals(('module.path', 'ClassName'), result)

    def testProperManagerShouldBeSet(self):
        surgery1 = Surgery(
            'transplant.tests.models.TestModel',
            'transplant.surgeons.NopSurgeon'
        )
        self.assertEquals(TestModel.objects, surgery1.manager)
        
        surgery2 = Surgery(
            'transplant.tests.models.TestModel',
            'transplant.surgeons.NopSurgeon',
            **{'manager': 'other_manager'}
        )
        self.assertEquals(TestModel.other_manager, surgery2.manager)
    
    def testProperSurgeonShouldBeSet(self):
        surgery1 = Surgery(
            'transplant.tests.models.TestModel',
            'transplant.surgeons.NopSurgeon',
        )
        self.assertEquals('NopSurgeon', surgery1.surgeon.__class__.__name__)
        
        surgery2 = Surgery(
            'transplant.tests.models.TestModel',
            'transplant.surgeons.DefaultSurgeon',
        )
        self.assertEquals('DefaultSurgeon', surgery2.surgeon.__class__.__name__)
    
    def testImproperlyConfiguredSouldBeRaisedIfModelCannotBeLoaded(self):
        with self.assertRaises(ImproperlyConfigured):
            Surgery(
                'non.existing.Model',
                'transplant.surgeons.NopSurgeon'
            )
    
    def testImproperlyConfiguredShouldBeRaisedIfManagerDoesNotExtist(self):
        with self.assertRaises(ImproperlyConfigured):
            Surgery(
                'transplant.tests.models.TestModel',
                'transplant.surgeons.DefaultSurgeon',
                **{'manager': 'so_wrong'}
            )
    
    def testImproperlyConfiguredShouldBeRaisedIfSurgeonCannotBeLoaded(self):
        with self.assertRaises(ImproperlyConfigured):
            Surgery(
                'transplant.tests.models.TestModel',
                'non.existing.Surgeon'
            )
    
    def testMergeShouldCallMergeOnSurgeon(self):
        surgery = Surgery(
            'transplant.tests.models.TestModel',
            'transplant.surgeons.NopSurgeon',
        )
        surgery.surgeon = Mock(surgery.surgeon)
        receiver = User.objects.create_user(username='receiver', password='pwd')
        donor = User.objects.create_user(username='donor', password='pwd')
        surgery.merge(receiver, donor)
        surgery.surgeon.merge.assert_called_with(receiver, donor)

class TransplantMergeViewTest(TransactionTestCase):
    urls = 'transplant.urls'
    
    def setUp(self):
        self.receiver = User.objects.create_user(username='receiver', password='p')
        self.donor = User.objects.create_user(username='donor', password='p')
        self.factory = RequestFactory()
        
        for i in range(0,10):
            u = self.receiver if i % 2 == 0 else self.donor
            TestModel(user=u).save()
            CustomUserFieldNameModel(person=u).save()
    
    def testFormValidShouldPeformMergeIfUserCanAuthenticate(self):
        request = self.factory.post('/', {'username': 'donor', 'password': 'p'})
        request.user = self.receiver
        v = TransplantMergeView()
        v.request = request
        
        with self.settings(
            TRANSPLANT_OPERATIONS = (
                ('transplant.tests.models.TestModel', 'transplant.surgeons.DefaultSurgeon', {}),
            )
        ):
            form = v.form_class(request)
            form.user_cache = self.donor
            v.form_valid(form)
            for m in TestModel.objects.all():
                self.assertEquals(self.receiver, m.user)
    
    def testFormValidShouldRollackIfAnyExceptionOccurs(self):
        request = self.factory.post('/', {'username': 'donor', 'password': 'p'})
        request.user = self.receiver
        
        with self.settings(
            TRANSPLANT_OPERATIONS = (
                ('transplant.tests.models.TestModel', 'transplant.surgeons.DefaultSurgeon', {}),
                (
                    'transplant.tests.models.CustomUserFieldNameModel',
                    'transplant.tests.surgeons.FaultySurgeon',
                    {'user_field': 'person'}
                ),
            )
        ):
            users_before_transaction = [m.user for m in TestModel.objects.all()]
            with self.assertRaises(RuntimeError):
                TransplantMergeView.as_view()(request)
            users_after_transaction = [m.user for m in TestModel.objects.all()]
            self.assertListEqual(users_before_transaction, users_after_transaction)
    
    def testExceptionReRaisedIfSettingsDebugIsTrue(self):
        request = self.factory.post('/', {'username': 'donor', 'password': 'p'})
        request.user = self.receiver
        
        with self.settings(
            TRANSPLANT_OPERATIONS = (
                (
                    'transplant.tests.models.TestModel',
                    'transplant.tests.surgeons.FaultySurgeon',
                    {'user_field': 'person'}
                ),
            ),
            DEBUG = True
        ):
            with self.assertRaises(RuntimeError):
                TransplantMergeView.as_view()(request)
    
    def testExceptionReRaisedIfFailureRedirectNotSet(self):
        request = self.factory.post('/', {'username': 'donor', 'password': 'p'})
        request.user = self.receiver
        
        with self.settings(
            TRANSPLANT_OPERATIONS = (
                (
                    'transplant.tests.models.TestModel',
                    'transplant.tests.surgeons.FaultySurgeon',
                    {'user_field': 'person'}
                ),
            ),
            DEBUG = False
        ):
            with self.assertRaises(RuntimeError):
                TransplantMergeView.as_view()(request)
    
    def testRedirectOnExceptionIfDebugFalseAndFailureRedirectSet(self):
        request = self.factory.post('/', {'username': 'donor', 'password': 'p'})
        request.user = self.receiver
        
        with self.settings(
            TRANSPLANT_OPERATIONS = (
                (
                    'transplant.tests.models.TestModel',
                    'transplant.tests.surgeons.FaultySurgeon',
                    {'user_field': 'person'}
                ),
            ),
            TRANSPLANT_FAILURE_URL = 'http://www.example.org',
            DEBUG = False
        ):
            response = TransplantMergeView.as_view()(request)
        self.assertEquals(302, response.status_code)