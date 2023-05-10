concateArray(X):- concatenation(X), hasInput(X,Y), array(Y).
concateSingleValue(X):- concatenation(X), hasInput(X,Y), singleValue(Y).

concateSingleValueOnly(X):-concateSingleValue(X), not concateArray(X).

%% concateWithSVOnlyFalse(X) :- concateSingleValueOnly(X), #count{Y: hasInput(X,Y)}<2.





