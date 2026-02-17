import unittest
from gen_content import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title_simple(self):
        result = extract_title("# Hello this is a test")
        self.assertEqual(result, "Hello this is a test")

    
    def test_extract_title_exception_not_h1(self):
        markdown = "## This is a header, but not h1"
        with self.assertRaises(Exception):
            extract_title(markdown)


    def test_extract_title_exception_no_heading(self):
        markdown = "This is not a heading"
        with self.assertRaises(Exception):
            extract_title(markdown)