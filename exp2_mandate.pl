dataProcessing(X) :- concatenation(X).
dataProcessing(X) :- weightedSum(X).
task(X) :- dataProcessing(X).
task(X) :- mlTraining(X).
task(X) :- mlTesting(X).

hasStartDpTask(X,Y) :- hasStartTask(X,Y), dataProcessing(Y).

hasNextDpTaskSeq(X,Y) :- hasNextTask(X,Y), dataProcessing(Y).
hasNextDpTaskSeq(X,Z) :- hasNextDpTaskSeq(X,Y), hasNextDpTaskSeq(Y,Z).

hasNextMltrainTaskSeq(X,Y) :- hasNextTask(X,Y), mlTraining(Y).
hasNextMltrainTaskSeq(X,Z) :- hasNextMltrainTaskSeq(X,Y), hasNextMltrainTaskSeq(Y,Z).

hasNextMltestTaskSeq(X,Y) :- hasNextTask(X,Y), mlTesting(Y).
hasNextMltestTaskSeq(X,Z) :- hasNextMltestTaskSeq(X,Y), hasNextMltestTaskSeq(Y,Z).


intermediateTask(X) :- task(X), hasNextTask(X,Y), task(Y).
endTask(X) :- task(X), not intermediateTask(X).

% hasNextTaskSeq(X,Y) :- hasNextTask(X,Y).
% hasNextTaskSeq(X,Z) :- hasNextTask(X,Y), hasNextTask(Y,Z).
% hasNextTaskSeq(X,Z) :- hasNextTaskSeq(X,Y), hasNextTask(Y,Z).


validMlPipeline(X):- hasStartDpTask(X,Y), hasNextDpTaskSeq(Y,T1), hasNextMltrainTaskSeq(T1,T2), hasNextMltestTaskSeq(T2,Z), endTask(Z).
validMlPipeline(X):- hasStartDpTask(X,Y), hasNextDpTaskSeq(Y,T1), hasNextMltestTaskSeq(T1,Z), endTask(Z).
% validMlPipeline(X):- hasStartDpTask(X,Y), dataProcessing(Y), hasNextTaskSeq(Y,Z), endTask(Z), mlTesting(Z).
falseMlPipeline(X):- mlPipeline(X), not validMlPipeline(X).


