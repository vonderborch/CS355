#lang scheme
(define (nth L i)
  (if (= i 0)
      ; if i == 0, return the head of the list and end search
      (car L)
      ; otherwise keep going through the list until the ith item is reached
      (nth (cdr L) (- i 1))
  )
)