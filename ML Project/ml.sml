(* ml.sml
 * Christian Webber
 * ML Programming Assignment
 * Programmed with Poly/ML for Windows
 * use "ml.sml";
 *)

(* **************************************************** *)
(* ******************** IN LIST *********************** *)
(* **************************************************** *)

(* in_list
 * Type: "Main" Function
 * Input: Variable x and a list
 * Output: A boolean whether x is in the list
 *)
fun in_list (x, []) = false
 	| in_list (x, y::r) =
 		if x = y then true
 		else in_list (x, r)

(* **************************************************** *)
(* ***************** INTERSECTION ********************* *)
(* **************************************************** *)

(* intersection
 * Type: "Main" Function
 * Input: Two lists, aL and bL
 * Output: A list of items that both lists contain
 *
 * Inner Function: loop: takes an output list and an input list
 *			 returns an intersection of the two lists.
 *)
fun intersection (aL, bL) = let
  	fun loop (out, []) = out
  	  | loop (out, x::r) =
 		if in_list (x, bL) then
 			if in_list (x, out) then loop (out, r)
 			else loop (x::out, r)
 		else loop (out, r)
 	in loop ([], aL)
 end

(* **************************************************** *)
(* ********************* UNION ************************ *)
(* **************************************************** *)

(* union
 * Type: "Main" Function
 * Input: Two lists, aL and bL
 * Output: A list of items that either list contains
 *
 * Inner Function: loop: takes an output list and the two input lists
 *			 returns a union of the two lists.
 *)
fun union aL bL = let
  	fun loop (out, [], []) = out
  	  | loop (out, x::xr, y) =
  		if in_list (x, out) then loop (out, xr, y)
  		else loop (x::out, xr, y)
 	  | loop (out, x, y::yr) =
 		if in_list (y, out) then loop (out, x, yr)
 		else loop (y::out, x, yr)
 	in loop([], aL, bL)
 end

(* **************************************************** *)
(* ********************* FILTER *********************** *)
(* **************************************************** *)

(* filterLoop
 * Type: "Auxiliary" Function
 * Input: A predicate "function" and two lists (an input and output)
 * Output: Returns a reversed version of the output list
 *)
fun filterLoop (pred, [], []) = []
   | filterLoop (pred, [], out) = rev out
   | filterLoop (pred, x::r, out) =
 	if pred x then filterLoop(pred, r, x::out)
 	else filterLoop(pred, r, out)

(* filter
 * Type: "Main" Function
 * Input: A predicate "function" and a list
 * Output: Returns an ordered list of all items in the passed list that are true for the predicate
 *)
fun filter pred L = filterLoop (pred, L, [])

(* **************************************************** *)
(* ******************* QUICKSORT ********************** *)
(* **************************************************** *)

(* quicksort
 * Type: "Main" Function
 * Input: A predicate "function" and a list
 * Output: Returns an ordered list of all items in the passed list that are true for the predicate
 *
 * Inner Function: partition: takes a predicate (pred), pivot (i), and list tuple ("rest" list, low list, high list)
 *			      returns an ordered (according to the predicate) list of the original lits.
 *)
fun quicksort pred [] = []
 	| quicksort pred (i::L) = let
 		fun partition pred i ([], low, high) = (quicksort pred low) @ [i] @ (quicksort pred high)
 		  | partition pred i (x::r, low, high) =
 			if pred (x, i) then partition pred i (r, x::low, high)
 			else partition pred i (r, low, x::high)
 	in partition pred i (L, [], [])
 end

(* **************************************************** *)
(* ************ PRACTICE WITH DATATYPES *************** *)
(* **************************************************** *)

(* either: A datatype where a variable can either be a string or an int *)
datatype either = ImAString of string | ImAnInt of int

(* eitherTree: A datatype where a variable can either be empty, a leaf of type either, or a node on a tree *)
datatype eitherTree = Empty | Leaf of either | Node of eitherTree * eitherTree

(* eitherSearch
 * Type: "Main" Function
 * Input: a tree item and an (int) value to search for
 * Output: whether the value is found in the tree
 *)
 
fun eitherSearch Empty x = false
   | eitherSearch (Node(l,r)) x =
 	(eitherSearch l x) orelse (eitherSearch r x)
   | eitherSearch (Leaf(v)) x =
 	case v of ImAString v => false
 		| ImAnInt v => x = v
		
(* eitherTest
 * Type: "Main" Function
 * Input: Nothing
 * Output: A boolean tuple containing the results of the first search and the second.
 *)
fun eitherTest () = ((eitherSearch (Node(Node(Node(Node(Leaf(ImAnInt 1),Leaf(ImAnInt 2)),Node(Leaf(ImAnInt 3),Leaf(ImAnInt 4))),Node(Node(Leaf(ImAnInt 5),Leaf(ImAString "a")),Node(Leaf(ImAString "b"),Leaf(ImAString "c")))), Node(Node(Leaf(ImAString "d"),Leaf(ImAString "e")),Empty))) 1), (eitherSearch (Node(Node(Node(Node(Leaf(ImAnInt 1),Leaf(ImAnInt 2)),Node(Leaf(ImAnInt 3),Leaf(ImAnInt 4))),Node(Node(Leaf(ImAnInt 5),Leaf(ImAString "a")),Node(Leaf(ImAString "b"),Leaf(ImAString "c")))), Node(Node(Leaf(ImAString "d"),Leaf(ImAString "e")),Empty))) 99))

(* **************************************************** *)
(* ***************** TREE TO STRING ******************* *)
(* **************************************************** *)

(* Tree: A polymorphic tree *)
datatype 'a Tree = LEAF of 'a | NODE of ('a Tree) list

(* treeToString
 * Type: "Main" Function
 * Input: a predicate function and a tree of datatype 'a
 * Output: A parenthesized string representing the string based on the predicate function.
 *)
fun treeToString pred (LEAF(v)) = pred v
   | treeToString pred (NODE(L)) = "(" ^ String.concat(List.map (treeToString pred) L) ^ ")"


(* **************************************************** *)
(* ********************* PERMS ************************ *)
(* **************************************************** *)

(* insert
 * Type: "Auxiliary" Function
 * Input: the value to rotate and the list to rotate it in
 * Output: the rotated lists
 *)
 fun insert x [] = [[x]]
  | insert x (y::ys) = let
	fun consy l = y::l
	in (x::y::ys)::(map consy (insert x ys)) end

(* perms
 * Type: "Main" Function
 * Input: a list
 * Output: a list of all permutations of the list
 *)
fun perms [] = [[]]
  | perms (x::xs) = List.concat(map (insert x) (perms xs))