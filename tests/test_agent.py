import unittest
import sys
import os

from owk_poc.agent import Agent


class TestAgent(unittest.TestCase):
    """
    Test suite for the Cancer Data Agent POC.
    Verifies the agent's response to various natural language queries.
    """

    def setUp(self):
        """Initialize the agent before each test."""
        self.agent = Agent()

    def test_help_command(self):
        """Test that 'help', 'assist', or 'support' triggers the help message."""
        response = self.agent.process_query("Can you help me?")
        self.assertIn("help", response.lower()) 
        self.assertIn("lung", response)

    def test_targets(self):
        """Test retrieving targets for a known cancer (lung)."""
        response = self.agent.process_query("What are the targets for lung cancer?")
        self.assertIn("lung", response.lower())
        self.assertIn("ALK", response) 

    def test_expression(self):
        """Test retrieving expression values for breast cancer."""
        response = self.agent.process_query("What is the median expression for breast cancer?")
        self.assertIn("breast", response.lower())
        self.assertIn("expression values", response.lower())
        self.assertTrue(any(char.isdigit() for char in response), "Response should contain numeric expression values")

    def test_unknown_cancer(self):
        """Test handling of a cancer type not in the dataset."""
        response = self.agent.process_query("Tell me about esophageal")
        self.assertIn("don't have information", response)
        self.assertIn("lung", response) 

    def test_discovery(self):
        """Test that the agent finds melanoma (which is in the CSV but maybe not hardcoded)."""
        response = self.agent.process_query("genes in melanoma")
        self.assertIn("melanoma", response.lower())
        self.assertIn("genetic targets", response.lower())

    def test_multi_cancer_query(self):
        """Test that a query matching multiple cancers returns information for all of them."""
        response = self.agent.process_query("breast and lung cancer")
        self.assertIn("breast", response.lower())
        self.assertIn("lung", response.lower())
        self.assertIn("ALK", response)    # From lung
        self.assertIn("BRCA1", response)  # From breast

if __name__ == '__main__':
    unittest.main()
