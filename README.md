# CS355
Projects for CS355 (Programming Language Design) at WSU, taught by Carl Hauser during Fall 2013.

These projects were programed using a variety of languages but were universally run on a Windows machine (although there shouldn't be any reason for them to not run on other platforms with proper compilers).

Projects:
- ML Project: Programmed with Poly/ML for Windows
  - ml.sml: 
    - in_list(x, []): Checks whether the variable x is in the list [].
    - intersection(aL, bL): Returns the intersection of the two provided lists.
    - union aL bL: Returns the union of the two provided lists.
    - filter(pred, [], []): Returns a reversed version of input list using the provided predicated function (pred).
    - quicksort pred []: Returns an ordered list based on the original provided list and predicate function.
    - eitherSearch Empty x: Outputs whether a value (x) is found in the tree (Empty) or not.
    - eitherTest: tests eitherSearch.
    - treeToString pred (LEAF(V)): Converts a tree (LEAF(V)) to a string using the predicate function (pred).
    - insert x []: Outputs a list rotated around the value x.
    - perms []: Outputs a list of all permutations of the provided list.
  - test.sml: Creates a tree with leaves and nodes to use for testing functions in ml.sml.
- Project One: Implements various encryption/decryption functions to solve an encrypted string (solved string is at the bottom).
  - Basic Functions Implemented:
    - maketable(s1, s2): Returns a dictionary mapping s1 to s2.
    - trans(ttable, s): Translates a string using the provided translation table (which is provided by maketable).
    - histo(s): Computes the histogram for the given string.
    - digraphs(s): Computs a list containing the number of times each digraph occurs in the string s.
    - main: Uses some testing functions to test the above functions.
- Project Three: Programmed with Scheme using DrRacket on Windows 8.
  - fold.rkt: Implements the foldr and foldl higher-order functions ( http://en.wikipedia.org/wiki/Fold_%28higher-order_function%29 ).
  - merge2.rkt: Implements a function that merges two lists of integers (already in ascending order) into a new list that is also in ascending order.
  - mergeN.rkt: Implements a function that takes a list of lists (each in ascending order already) into a new list containing all of the elements of the provided lists.
  - nth.rkt: Implements a function that returns the nth element of a list (0-based indexing).
  - range.rkt: Implements a that returns a list of integers between the minimum (inclusive) and the maximum (exclusive).
  - repl.rkt: Returns a new list that is the same as the original but changes a single value in the list to a new value.
  - scheme.rkt: contains all the above functions.
  - c-webber_scheme_assignment.txt: contains all the above functions.
- Lander: Implements a basic 'moon lander' game in Java.
- SPS-test cases: The completed SPS code (see SPS) including test case programs.
- SPS-working: A folder containing various stages of development for my SPS implementation.
- SPS: Implements an interpreter for a PostScript-like language (assignment and language specifications listed in firstInterpreterAssignment.pdf in the directory). Some example programs can be found in the SPS-test cases folder.
- SSPS: Reimplementation of the SPS interpreter to handle a static-scoped version of the language as well as the default dynamic scoped version. Assignment and language specifications can be found in the ssps.pdf file in the directory.
