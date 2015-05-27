#lang scheme
(define (range min max)
  (if (= min max)
      ; if min == max, we've already reached the last #, so return an empty list and end
      '()
      ; otherwise, return the current # and continue going through the list
      (cons min (range (+ min 1) max))
  )
)