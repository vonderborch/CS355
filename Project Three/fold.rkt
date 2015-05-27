#lang scheme
(define (fold fcombine basecase L) 
   (cond
      ((null? L) basecase)
      (#t (fcombine (car L) (fold fcombine basecase (cdr L))))
   ))
(define foldr fold)
(define (foldl fcombine basecase L)
   (cond
      ((null? L) basecase)
      (#t (foldl fcombine (fcombine (car L) basecase ) (cdr L)))
   ))

