import sys
import unittest

import Kysy

import PythonTest

print "\nRunning PythonLoggerCallBack Unit Test"

class PythonLoggerCallBack(Kysy.LoggerCallBack):
  def __init__(self):
    super(PythonLoggerCallBack, self).__init__()

  def log(self, message, log_level, component ):
    self.message = message
    self.logLevel = log_level
    self.component = component

class TestLoggerCallback(unittest.TestCase):

  def setUp(self):
    self.logger = PythonTest.platform.platformAccess().logger()
    self.python_call_back = PythonLoggerCallBack()
    self.logger.callBack( self.python_call_back )

  def test_python_call_back(self):
    self.logger.log( "Python Message", Kysy.Logger.LOG_ERROR, "Python Component" )
    self.assertEqual( "Python Message", self.python_call_back.message )
    self.assertEqual( "Python Component", self.python_call_back.component )
    self.assertEqual( Kysy.Logger.LOG_ERROR, self.python_call_back.logLevel )

  def tearDown(self):
    self.logger.removeCallBack( self.python_call_back )

if __name__ == '__main__':
      unittest.main( argv=sys.argv[:1] )

# vim:ts=2:sw=2:et
