import unittest
from assembler import Assembler

class AssemblerTest(unittest.TestCase):
	def runTest(self):
		assembler = Assembler()
		self.test_reg_to_binary(assembler)
		self.test_int_to_binary(assembler)
		self.test_twos_complement(assembler)
		self.test_binary_to_hex(assembler)

	def test_reg_to_binary(self, assembler):
		input = "r3"
		expected = "0011"
		result = assembler.reg_to_binary(input, 4)
		self.assertEqual(expected, result)

	def test_int_to_binary(self, assembler):
		input = 15
		expected = "1111"
		result = assembler.int_to_binary(input, 4)
		self.assertEqual(expected, result)

	def test_twos_complement(self, assembler):
		input = "0000010001110001"
		expected = "1111101110001111"
		result = assembler.remove_negative(input)
		self.assertEqual(expected, result)

	def test_binary_to_hex(self, assembler):
		input = "000101100001111100111110"
		expected = "161f3e"
		result = assembler.binary_to_hex(input)
		self.assertEqual(expected, result)

test = AssemblerTest().runTest()
