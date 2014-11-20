import unittest
import string
from provider import Command
from assembler import Assembler

class AssemblerTest(unittest.TestCase):
	def runTest(self):
		self.assembler = Assembler()
		self.test_reg_to_binary()
		self.test_int_to_binary()
		self.test_twos_complement()
		self.test_binary_to_hex()
		self.test_command()

	def test_reg_to_binary(self):
		input = "r3"
		expected = "0011"
		result = self.assembler.reg_to_binary(input, 4)
		self.assertEqual(expected, result)

	def test_int_to_binary(self):
		input = 15
		expected = "1111"
		result = self.assembler.int_to_binary(input, 4)
		self.assertEqual(expected, result)

	def test_twos_complement(self):
		input = "0000010001110001"
		expected = "1111101110001111"
		result = self.assembler.twos_complement(input, 16)
		self.assertEqual(expected, result)

	def test_binary_to_hex(self):
		input = "000101100001111100111110"
		expected = "161f3e"
		result = self.assembler.binary_to_hex(input)
		self.assertEqual(expected, result)

	def test_command(self):
		input = Command(["cmp","r2","r3"], 10, "0010")
		expected = "\t10\t\t\t:\t32012e;"
		result = self.assembler.r_type(input)
		self.assertEqual(expected, result)

test = AssemblerTest().runTest()
