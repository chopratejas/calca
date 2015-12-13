# calca
Calca is a text editor that takes in mathematical relationships and generates answers for you (Check calca.io).
For example:
a = 10
b = 20
z = a + b
z =>

This is a sample input given to the calca application and its output will be:
a = 10
b = 20
z = a + b
z => 30

By changing a and b, the value of z is updated. This is a very simple example, there are more complicated examples.

The current implementation is a very minimalistic implementation in python and supports only basic arithmetic operations.
The assumption is that a particular symbol is on only one side (either LHS or RHS) and not both. It is easy to modify the relationships to do so.

To run:
python <program_name> <input_file> <output_file>
