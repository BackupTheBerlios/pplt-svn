import edef
import unittest


class testDecorators(unittest.TestCase):
    
    def testArguments(self):
        @edef.BoolDecorator
        def bool_func(value): return "%s (%s)"%(value, type(value))

        self.assertEqual(bool_func("test"), "True (<type 'bool'>)")
        self.assertEqual(bool_func(""), "False (<type 'bool'>)")


    def testType(self):
        @edef.BoolDecorator
        def bool_func(value): return "%s (%s)"%(value, type(value))
       
        self.assertEqual(bool_func.dec_type_name, "bool")
