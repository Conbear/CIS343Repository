How I have statements is very simmilar to Lox with statements ending with ;.

All tests were tested with REPL and as files.

test 1
This was testing for errors about missing ;, incomplete expression in print statement, and missing () in print statement as well as making sure it checked everything in file and did not stop before it finished the file.

input:
"one"
true;
print 2 +

expected output:
Error: Syntax error: Expect ';' at the end of the statement on line [1] while parsing
Error: Syntax error: Expect '(' after 'print'. on line [3] while parsing
Error: missing right operand after + at token 3 on line [3] while parsing
Error: Syntax error: Expect ')' after print expression. on line [3] while parsing
Error: Syntax error: Expect ';' at the end of the statement on line [3] while parsing

actual output:
Error: Syntax error: Expect ';' at the end of the statement on line [1] while parsing
Error: Syntax error: Expect '(' after 'print'. on line [3] while parsing
Error: missing right operand after + at token 3 on line [3] while parsing
Error: Syntax error: Expect ')' after print expression. on line [3] while parsing
Error: Syntax error: Expect ';' at the end of the statement on line [3] while parsing

The expected output was the same as the actual output with all errors properly reported.

test2
This was testing to see if nothing would print when a statement was entered on its own, strings are printed properly with the print statement, boolean is printed properly with the print statement, expressions are evaluated and printed properly with print statement, and nil type is printed properly with the print statement.

input:
4 + 2;
print ("one");
print (true);
print (1 + 2);
print (nil);

expected output:
one
true
3.0
Nil

actual output:
one
true
3.0
Nil

The expected output was the same as the actual output with no errors reported.

There was no test that failed and no known limitations.