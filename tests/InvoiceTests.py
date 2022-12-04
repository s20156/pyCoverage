import json
import re
import unittest

from assertpy import *

from Invoice import *

class InvoiceTests(unittest.TestCase):
    def setUp(self) -> None:
        invoice_file = open("../Invoice.json")
        plays_file = open("../Plays.json")
        self.invoice = json.loads(invoice_file.read())
        self.plays = json.loads(plays_file.read())
        self.dollar_regexp = r'\$\d*\,?\d{3}.\d{2}[\s, \n]'


    def test_statement_returns_values(self):
        assert_that(statement(self.invoice, self.plays)).is_not_none()

    def test_statement_returns_valid_dollar_format(self):
        assert_that(statement(self.invoice, self.plays)).matches(self.dollar_regexp)

    def test_contains_price(self):
        print(statement(self.invoice, self.plays))
        assert_that(statement(self.invoice, self.plays)).contains("Amount owed is")

    def test_view_amount_of_credits(self):
        credits_regexp = r'You earned \d* credits'
        assert_that(statement(self.invoice, self.plays)).matches(credits_regexp)

    def test_hamlet(self):
        assert_that(statement(self.invoice, self.plays)).contains("Hamlet:")

    def test_no_macbeth(self):
        assert_that(statement(self.invoice, self.plays)).does_not_contain("Macbeth:")

    def test_raises_value_error(self):
        wrong_plays = {
            "hamlet": {"name": "Hamlet", "type": "test"},
            "as-like": {"name": "As You Like It", "type": "comedy"},
            "othello": {"name": "Othello", "type": "tragedy"}
        }
        assert_that(statement).raises(ValueError).when_called_with(self.invoice, wrong_plays)