validTask(X) :- weightedSum(X), hasInput(X,Y).
falseTaskWOInput(X) :- weightedSum(X), not validTask(X).
