; Christian Webber
; October 6th, 2013
; Scheme Assignment ("Homework 2")
; Programmed with DrRacket on Windows 8.

#lang scheme
; nth: takes a list and index #, returns the item in the list at the index #
(define (nth L n)
  (if (= n 0)
      ; if n == 0, return the head of the list and end search
      (car L)
      ; otherwise keep going through the list until the nth item is reached
      (nth (cdr L) (- n 1))
  )
)

; repl: takes a list, an index #, and an item, returns a list identical to the original 
;       aside from the item at the index, which becomes the new item
(define (repl L i v)
  (if (null? L)
      ; if the list is empty, return an empty list and end
      '()
      ; otherwise...
      (if (= i 0)
          ; if i == 0, return v instead of the head of the list, and go through the rest of 
          ; the list.
          (cons v (repl (cdr L) (- i 1) v))
          ; otherwise, return the head of the list before going through the rest of the list
          (cons (car L) (repl (cdr L) (- i 1) v))
      )
  )
)

; range: takes a min and a max, returns a list of numbers ranging from the min to the max-1
(define (range min max)
  (if (= min max)
      ; if min == max, we've already reached the last #, so return an empty list and end
      '()
      ; otherwise, return the current # and continue going through the list
      (cons min (range (+ min 1) max))
  )
)

; merge2: Merges two lists in ascending order and returns/merges them into a new list also 
;         in ascending order
(define (merge2 A B)
  (if (null? A)
      (if (null? B)
          ; done with both lists
          '()
          ; done with list A, but not list B
          (cons (car B) (merge2 '() (cdr B)))
      )
      (if (null? B)
          ; done with list B, but not list A
          (cons (car A) (merge2 (cdr A) '()))
          ; not done with either list
          (if (< (car A) (car B))
              ; front of list A less than front of list B
              (cons (car A) (merge2 (cdr A) B))
              ; front of list B less than front of list A, or equal
              (cons (car B) (merge2 A (cdr B)))
          )
      )
  )
)

; mergeN: takes a list of lists of any length and returns/merges them in ascending order.
(define (mergeN L)
  (fold merge2 '() L)
)



; Although foldr is defined within scheme on my computer, in case it isn't for everyone,
; this is the definition of foldr as given in the classroom.
(define (fold fcombine basecase L) 
   (cond
      ((null? L) basecase)
      (#t (fcombine (car L) (fold fcombine basecase (cdr L))))
   ))
