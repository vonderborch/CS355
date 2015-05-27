#lang scheme
(define (repl L i v)
  (if (null? L)
      ; if the list is empty, return an empty list and end
      '()
      ; otherwise...
      (if (= i 0)
          ;if i == 0, return v instead of the head of the list, and go through the rest of the list
          (cons v (repl (cdr L) (- i 1) v))
          ; otherwise, return the head of the list before going through the rest of the list
          (cons (car L) (repl (cdr L) (- i 1) v))
      )
  )
)