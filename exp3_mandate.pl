concateArray(X):- concatenation(X), hasInput(X,Y), array(Y).
concateSingleValue(X):- concatenation(X), hasInput(X,Y), singleValue(Y).

concateArrayOnly(X):-concateArray(X), not concateSingleValue(X).
concateSingleValueOnly(X):-concateSingleValue(X), not concateArray(X).

falseConcateInputType(X) :- concatenation(X), not concateArrayOnly(X), not concateSingleValueOnly(X).


