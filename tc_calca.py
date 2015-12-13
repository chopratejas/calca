__author__ = 'tejas'
import os
import re
import sys

# This file contains a bare-minimum implementation of calca. For more: visit calca.io
# It takes in an input file and generates an output file where the RHS of => contains the solution
# of the equation.
# The basic idea is to maintain a symbol table (in the form of a dictionary). The key for this symbol table will
# be the different symbols & the values would be their corresponding values.
# For example: x = 5 --> key = x, value = 5
#              z = a + b --> key = z, value = a + b
# For the purpose of simplified implementation, there are a bunch of assumptions made
# 1. the LHS of '=' will have only one symbol. thus x / y = 5 is not supported. This can be written as x = 5 * y.
# 2. every line that contains '=' or '=>' should have a 'sane' arithmetic operation. We use 'eval' to evaluate the
#    arithmetic operations assuming they are sane, else we'd have to use numPy, it is mentioned as a todo
# 3. We have used simple regex search based on a few examples. More complicated and complete regex searches could be
#    performed.
# 4. The input file should consist of only simple basic arithmetic ops: +,-,*,/


# Delimiters would help separate the symbols from the operations to be performed on them.
# They are just a list of arithmetic operations and () brackets.
delimiters = ['+', '-', '*', '/', '(', ')', '']


# Check whether a given string is a number or not.
def is_number(s):
    try:
        float(s)        # for int, long and float
    except ValueError:
        try:
            complex(s)  # for complex
        except ValueError:
            return False
    return True


# Given a symbol, evaluate its value and store it inside the dictionary.
def evaluate_symbol(sym, symtable):
    # Check if the symbol key is in the dictionary.
    if sym not in symtable.keys():
        print "Error: Improper symbol %s" % sym
        sys.exit(1)

    # Obtain the value from the dictionary.
    v = str(symtable.get(sym))

    # If the value at the 'sym' key is an integer, place the integer in the dictionary.
    if is_number(v):
        symtable[sym] = int(v)


# This function will be given an input string and it will split the string into
# several parts, each part will either be a symbol or an operation. The splitting
# is done by observing the delimiters.
# TODO: This can be optimized by using regex and string splits.
def create_list(m, symtable):
    val = ""
    v = []

    # If it is a number, the list just comprises that.
    if is_number(m):
        v.append(m)
        return v

    for c in m:
        # As long as any delimiter is not encountered, the characters
        # are appended to a value.
        if c not in delimiters:
            val = val + c
        else:
            # At this point, we have encountered a delimiter (which are just arithmetic ops).
            # Hence, the 'val' accumulated till now is stripped of starting and ending whitespace
            # and it is appended to a list.
            if val != "":
                val = val.rstrip()
                val = val.lstrip()
                v.append(val)
            v.append(c)
            val = ""

    # The last 'val' is taken care of
    val = val.rstrip()
    val = val.lstrip()
    v.append(val)
    return v


# Given an input string, this function will evaluate the symbols of that string.
def eval_sym_str(m, symtable):

    # Create a list of all symbols and operations.
    v = create_list(m, symtable)

    for i in v:
        # If the element in the list is a symbol, populate its value in the dictionary.
        if i in symtable.keys():
            evaluate_symbol(i, symtable)
        else:
            # If the element is not a symbol in the dictionary, then it has to be
            # a delimiter or an integer value, else we have a faulty input code.
            if i not in delimiters and not is_number(i):
                print "Error: Improper symbol :%s" % i
                sys.exit(1)


# This function will perform the arithmetic operations to obtain the value of a symbol.
def perform_operation(m, symtable):
    # Create a list of all symbols and operations.
    v = create_list(m, symtable)
    new_v = ""

    # Check every element in the list
    for i in v:
        # If the element belongs to the dictionary, obtain its value.
        # The value might itself be comprising symbols in which case, perform the arithmetic
        # operation on the symbols.
        #print i
        if i in symtable.keys():
            #print "%s->%s" %(i, symtable.get(i))
            if i in str(symtable.get(i)):
                print "%s = %s" %(i, symtable.get(i))
                print "TODO: Cannot support this for now. Try changing the input to have same symbols on same side."
                sys.exit(1)
            new_v += str(perform_operation(symtable.get(i), symtable))
        else:
            # If the element is not in the dictionary, then it should be an operation
            # or an integer.
            if i not in delimiters and not is_number(i):
                print "Error: Improper symbol: %s" % i
                sys.exit(1)
            else:
                new_v += str(i)
    # At this point, the new_v will contain the arithmetic statement to be executed.
    # It can directly be evaluated.
    # TODO: The arithmetic statement could be faulty too, in which case it is advisable to use numPy instead of eval.
    return eval(new_v)


def parse_and_eval_file(infile, outfile):

    symtable = {}

    # For every line in the file, if it contains '=', populate a symbol table
    # the key for which is the symbol and the value is the value on the RHS of '='.
    # Both the key and the value may or may not contain integer/float values.
    for i in infile:
        # Skip a line if it doesnt have '=' or '=>'
        if "=" not in i and "=>" not in i:
            outfile.write(i)
            continue

        # Populate the symbol table.
        if "=>" not in i:
            outfile.write(i)
            match = re.search(r'(.*?)\s*=\s*(.*$)', i)
            if match:
                symtable[match.group(1)] = match.group(2)
            else:
                print "Incorrect format : %s" % i
        else:
            # Evaluate a symbol string.
            match = re.search(r'(.*?)\s*=>', i)
            line = ""
            if match:
                eval_sym_str(match.group(1), symtable)
                # Perform the operation and direct the result to an output file specified.
                line = str(match.group(1)) + " => " + str(perform_operation(match.group(1), symtable))
                outfile.write(line)
                outfile.write("\n")
            else:
                print "Incorrect format : %s" % i


def main():
    # Check if the script is called properly.
    if len(sys.argv) != 3:
        print "Error: Usage: tc_calca.py input_file output_file"
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    try:
        input_file = os.path.abspath(input_file)
        output_file = os.path.abspath(output_file)
        infile = open(input_file, 'r')
        outfile = open(output_file, 'w')
        parse_and_eval_file(infile, outfile)
    except (OSError, IOError) as e:
        print "Error: File %s is either not present or cannot be read" % input_file
        sys.exit(1)
    infile.close()
    outfile.close()


if __name__ == '__main__':
    main()
