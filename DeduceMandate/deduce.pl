pipeline(x) :- mlPipeline(x).


%%# exp1: all tasks should have input
dataProcessing(X) :- concatenation(X).
dataProcessing(X) :- weightedSum(X).
task(X) :- dataProcessing(X).
task(X) :- mlTraining(X).
task(X) :- mlTesting(X).
dataEntity(X) :- array(X).
dataEntity(X) :- singleValue(X).
dataEntity(X) :- structure(X).

instance(x) :- pipeline(x).
instance(x) :- task(x).
instance(x) :- dataEntity(x).
instance(x) :- method(x).

objectProperty(x,y) :- hasNextTask(x,y).
objectProperty(x,y) :- hasStartTask(x,y).
objectProperty(x,y) :- hasInput(x,y).
objectProperty(x,y) :- hasOutput(x,y).
dataProperty(x,y) :- hasDimension(x,y).
objectProperty(x,y) :- hasLength(x,y).

%%# validTask(X) :- task(X), hasInput(X,Y).
%%# falseTaskWOInput(X) :- task(X), not validTask(X).

%%# exp2: mlpipeline = dataProcessing* + mlTraining* + mlTesting*
%%# DEDUCE 	DataProcessing
%%# MANDATE 	[1,*](hasNextTask.DataProcessing).[1,*](hasNextTask.MLTesting) OR 
%%# (hasNextTask.DataProcessing)[1,*].(hasNextTask.MLTraining)[0,*].(hasNextTask.MLTesting)[1,*]

%%# hasStartDpTask(X,Y) :- hasStartTask(X,Y), dataProcessing(Y).

%%# hasNextDpTaskSeq(X,Y) :- hasNextTask(X,Y), dataProcessing(Y).
%%# hasNextDpTaskSeq(X,Z) :- hasNextDpTaskSeq(X,Y), hasNextDpTaskSeq(Y,Z).

%%# hasNextMltrainTaskSeq(X,Y) :- hasNextTask(X,Y), mlTraining(Y).
%%# hasNextMltrainTaskSeq(X,Z) :- hasNextMltrainTaskSeq(X,Y), hasNextMltrainTaskSeq(Y,Z).

%%# hasNextMltestTaskSeq(X,Y) :- hasNextTask(X,Y), mlTesting(Y).
%%# hasNextMltestTaskSeq(X,Z) :- hasNextMltestTaskSeq(X,Y), hasNextMltestTaskSeq(Y,Z).

%%# intermediateTask(X) :- task(X), hasNextTask(X,Y), task(Y).
%%# endTask(X) :- task(X), not intermediateTask(X).

%%# validMlPipeline(X):- hasStartDpTask(X,Y), hasNextDpTaskSeq(X,T1), hasNextMltrainTaskSeq(T1,T2), hasNextMltestTaskSeq(T2,Z), endTask(Z).
%%# validMlPipeline(X):- hasStartDpTask(X,Y), hasNextDpTaskSeq(X,T1), hasNextMltestTaskSeq(T1,Z), endTask(Z).
%%# falseMlPipeline(X):- mlPipeline(X), not validMlPipeline(X).

%%# exp3: concatenation input should be the same structure
%%# DEDUCE 	y:Concatenation,y:SuperTask 
%%# MANDATE 	<1 hasInput.SingleValue) OR \forall hasInput.SingleValue
%%# AND
%%# DEDUCE 	y:Concatenation
%%# MANDATE 	not (>=1 hasInput [1,*].Array) OR \forall hasInput.Array
%%# AND
%%# DEDUCE 	y:Concatenation
%%# MANDATE 	(0,1]hasInput.Object OR \forall hasInput.Object

%%# concateArray(X):- concatenation(X), hasInput(X,Y), array(Y).
%%# concateSingleValue(X):- concatenation(X), hasInput(X,Y), singleValue(Y).

%%# concateArrayOnly(X):-concateArray(X), not concateSingleValue(X).
%%# concateSingleValueOnly(X):-concateSingleValue(X), not concateArray(X).

%%# falseConcateInputType(X) :- concatenation(X), not concateArrayOnly(X), not concateSingleValueOnly(X).

%%# exp3.1: concatenation input should have at least two inputs

%%# concateInput(X,Y) :- concatenation(X), hasInput(X,Y), dataEntity(Y).
%%# falseConcateInputNum(X) :- concatenation(X), #count{Y: concateInput(X,Y)}>4.

%% exp4 & exp5 : dimension match 

%%# DEDUCE	Concatenation
%%# COMPARE	Set{hasInput.hasDimension} :: Compare(=,hasConcatenatingDim) :: LogicAnd(#1)

%%# concateHasInputDimension(X,Y) :- concatenation(X), hasInput(X,Input), array(Input), hasDimension(Input, Y).
%%# concateHasOutputDimension(X,Y) :- concatenation(X), hasOutput(X,Input), array(Input), hasDimension(Input, Y).

%%# exp6: weightedSum input number matches weighted

