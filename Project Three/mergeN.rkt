#lang scheme
(define (mergeN L)
  (foldr merge2 '() L)
)

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
