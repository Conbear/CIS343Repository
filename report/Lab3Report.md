My expression grammar is very similar to lox. It follows the precidence of expression -> equality -> comparison -> term -> factor -> unary -> primary -> grouping with grouping going back to expression. There has been no grammar changes since Lab 2 but there was some changes in the error messages given to try to give more clarity about their cause including which part threw the error, scanner or parser, and the general area for where the error occured.

There are no special set up instructions for running tests other than having the test files and the main language file.

All test cases were tested as direct input and in file format with results being the same for both and errors not stopping the direct input.

Test cases were broken down into 2 groups, error testing to be sure error messages worked and functional testing to be sure aspects worked as intended.

test1
This was testing to see if it could take a basic equation and give an ast. This was also testing to see if multiple lines in a file could work and give different ast but was done so just to test it and all other test cases only had one line.

input:
1+2
1+3

expected output:
Structure: (+ 1 2)
Structure: (+ 1 3)

actual output:
Structure: (+ 1 2)
Structure: (+ 1 3)

The result matched the expectations and no unplanned errors were reported.

test2
This was testing to see if more complex input with multiple operators and worked in combination with test3 to see if simple precidence worked. The point was to have the ast be correct for the input and the output be different from test3.

input: 1+2*3

expected output: Structure: (+ 1 (* 2 3))

actual output: Structure: (+ 1 (* 2 3))

The result matched the expectations and no unplanned errors were reported.

test3
This was working with test2 to see if precidence worked so that it would give different output from test2.

input: 1*2+3

expected output: Structure: (+ (* 1 2) 3)

actual output: Structure: (+ (* 1 2) 3)

The result matched the expectations and no unplanned errors were reported and precidensce worked as intended in this scenario.

test4
This was testing to see if unary, binary and grouping with a nested binary in it worked.

input: -123*(45.67+2)

expected output: Structure: (* (- 123) (group (+ 45.67 2)))

actual output: Structure: (* (- 123) (group (+ 45.67 2)))

The result matched the expectations and no unplanned errors were reported.

test5
This was testing to see if equality and comparrison worked along with testing to see if identifiers were properly treated as literals. This was also testing to see if unary worked with a group as its primary as well as having precidence be properly followed for all aspects at once.

input: -(-12)/ 3 +  4 <= 5 == apple

expected output: Structure: (== (<= (+ (/ (- (group (- 12))) 3) 4) 5) apple)

actual output: Structure: (== (<= (+ (/ (- (group (- 12))) 3) 4) 5) apple)

The result matched the expectations and no unplanned errors were reported.

test6
This was testing to see if true and false worked as literals.

input: true == 12 < false

expected output: Structure: (== true (< 12 false))

actual output: Structure: (== true (< 12 false))

The result matched the expectations and no unplanned errors were reported.

error1
This was testing to see if the error caused by missing the right operand of a binary would be properly reported.

input: 5 +

expected output: Error: missing right operand after + at token 2 on line [1] while parsing

actual output: Error: missing right operand after + at token 2 on line [1] while parsing

The result matched the expectations and only the planned error was reported.

error2
This was testing to see if the error caused by missing the left operand of a binary on its own would be properly reported.

input: * 2

expected output: Error: missing left operand before * at token 1 on line [1] while parsing

actual output: Error: missing left operand before * at token 1 on line [1] while parsing

The result matched the expectations and only the planned error was reported.

error3
This was testing to see if the error of an empty grouping is properly reported.

input: 5 * ()

expected output: Error: empty parenthesis with missing expression at token 3 on line [1] while parsing

actual output: Error: empty parenthesis with missing expression at token 3 on line [1] while parsing

The result matched the expectations and only the planned error was reported.

error4
This was testing to see if the error of an operator being where an operand should be is properly reported.

input: 5+/2

expected output: Error: Unexpected operator / at token 2 where operand was expected on line [1] while parsing

actual output: Error: Unexpected operator / at token 2 where operand was expected on line [1] while parsing

The result matched the expectations and only the planned error was reported.

error5
This was testing to see if the error of a missing operand for a unary would be reported.

input: -

expected output: Error: missing operand after unary - at token 1 on line [1] while parsing

actual output: Error: missing operand after unary - at token 1 on line [1] while parsing

The result matched the expectations and only the planned error was reported.

error6
This was testing to see if the error of an unclosed parenthesis would be reported.

input: (123+45

expected output: Error: Unclosed parenthesis on line [1] while parsing

actual output: Error: Unclosed parenthesis on line [1] while parsing

The result matched the expectations and only the planned error was reported.

error7
This was testing to see if the error of a closing parenthesis without a corresponding opening parenthesis would be reported.

input: 123+45)

expected output: Error: Unmatched right parenthesis at token 3 on line [1] while parsing

actual output: Error: Unmatched right parenthesis at token 3 on line [1] while parsing

The result matched the expectations and only the planned error was reported.

error8
This was testing to see if the error of a closing parenthesis at the start of the input would be reported.

input: )2+(3+4)

expected output: Error: Unmatched closing parenthesis ) at token 0 on line [1] while parsing

actual output: Error: Unmatched closing parenthesis ) at token 0 on line [1] while parsing

The result matched the expectations and only the planned error was reported.

error9
This was testing to see if the error of a string being used would be reported.

input: "friend" + 3

expected output: Error: Unexpected string "friend" at token 1 on line [1] while parsing

actual output: Error: Unexpected string "friend" at token 1 on line [1] while parsing

The result matched the expectations and only the planned error was reported.

error10
This was testing to see if the missing left operand error would be reported within a grouping.

input: 1-(* 2)

expected output: Error: missing left operand before * at token 4 on line [1] while parsing

actual output: Error: missing left operand before * at token 4 on line [1] while parsing

The result matched the expectation and only the planned error was reported.


Diagram:

1 == 3 - 2

                    expression
                    |
                    equality
                    |
        comparison < == > comparison
        |                   |
        <                   <
        term                term
        |                   |
        <           factor < - > factor
        factor      |              |
        |           <              <
        <           unary          unary
        unary       |              |
        |           primary        primary
        primary     |              |
        |           NUMBER         NUMBER
        NUMBER      |              |
        |           3              2
        1

ast for 1 == 3 - 2:
(== 1 (- 3 2))

Following the diagram from top to bottom, it shows that the first split is a == which means it is the first part of the ast (== comparison comparison). Then, following the left branch, it goes down to the left with no more splits and ends at the number 1 which gives us (== 1 comparison). After that, following the right branch from the split shows that there is a split at a -, giving us (== 1 (- factor factor)). Following the left at this split, it goes down with no more splits and ends at the number 3 which gives us (== 1 (- 3 factor)). Now we go down the right branch at the - and following it, there is no more splits and ends at the number 2 which gives us (== 1 (- 3 2)). Since there is no more nodes of the diagram, (== 1 (- 3 2)) is the ast.


There were no failing tests or known limitations.