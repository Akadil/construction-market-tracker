# write a test for the function getTextFromFile that checks if the function returns the expected output.

import unittest
from services.appendix_parser.GetTextFromFile import GetTextFromFile
from services.appendix_parser.CustomException import CustomException

class TestGetTextFromFile(unittest.TestCase):
    def test_getTextFromFile(self):
        # Create an instance of the class
        gtf = GetTextFromFile("test.pdf")
        # Test the function
        self.assertEqual(gtf.getTextFromFile(), "The text is not in the proper format")

if __name__ == '__main__':
    unittest.main()