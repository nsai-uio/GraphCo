# GraphCo
repo for the graph constraint language GraphCo, this repo contains all the codes for the experiments reported in the ISWC research paper.

# Dependency
1. Apache Spark   https://spark.apache.org/
2. Datalog endpoint: DLV     https://www.dlvsystem.it/dlvsite/dlv-user-manual/
3. python package:
  PySpark
  
  
# Experiment Content
The experiments are done using datalog and pyspark, which aim to evaluate the complexity of GraphCo in verifying KGs

There are 6 constraints included in the experiments, they are:
### 1. Each Task in the ML pipeline should have at least one DataEntity as input.
  expressed in GraphCo
  > DEDUCE Task
  > 
  > MANDATE [1 ,∗] hasInput . DataEntity
### 2. A valid ML pipeline should be the combination of a sequence of DataProcessing tasks, a sequence of MLTraing tasks and a sequence of MLTesting tasks. The MLTraing tasks are optional, while the other two sequences are mandatory.
  expressed in GraphCo
  > DEDUCE Task
  > 
  > MANDATE [1 ,∗]( hasNextTask . DataProcessing ) .[1 ,∗]( hasNextTask . MLTesting ) OR ( hasNextTask . DataProcessing ) [1 ,∗].( hasNextTask . MLTraining ) [1 ,∗].(
hasNextTask . MLTesting ) [1 ,∗]

### 3. All the input DataEntity of Concatenation tasks should be the same subclass of DataStructure, which means that they should all be Arrays or SingleValues.
  expressed in GraphCo
  > DEDUCE Concatenation
  > 
  > MANDATE ( NOT [1 ,∗]( hasInput . SingleFeature ) AND [1 ,∗] hasInput .
SingleFeature ) OR ( NOT [1 ,∗]( hasInput . Array ) AND [1 ,∗] hasInput . Array )
### 4. All the inputs dimension of the WeightedSum tasks should be same.
  expressed in GraphCo
  > DEDUCE WeightedSum
  > 
  > COMPARE hasInput . hasDimension :: Comp (= , hasInput . hasDimension ) :: LogicAnd
### 5. The number of inputs of the WeightedSum tasks should not be greater than the length of the weight vector for the tasks.
  expressed in GraphCo
  > DEDUCE WeightedSum
  > 
  > COMPARE hasInput :: Count :: Comp ( >=, hasWeightVector . Length )
### 6. The Concatenation tasks should have at least two SingleFeature as inputs, and the aggregation of the input dimension should be equal to the output dimension
  expressed in GraphCo
  > DEDUCE Concatenation . hasInput . SingleFeature
  > 
  > MANDATE [2 ,∗] hasInput . SingleFeature
  > 
  > COMPARE hasInput . Dimension :: Agg :: Comp (= , hasOutput . Dimension ) :: LogAnd


# How to run
1. generate KG randomly
  In DeduceMandate\:
  >python generateAbox.py -pipeline_number='pipeline number' -file_name='file name'
2. Run DEDUCE
  In DeduceMandate\: 
  >.\dlvWin.exe -stats 'file name' 'deduce.pl'
3. Run MANDATE
  In DeduceMandate\: 
  >.\dlvWin.exe -stats 'file name' 'exp1/2/3/6_mandate.pl'
4. generate tuples with literal information randomly
  In Compare\:
  >python generateTuples.py -task_name='task name' -task_num='task number' -file_name='file name'
6. Run Compare
  In Compare\:
  >python compareExpCsv.py -exp='constraint id' -task_num='task number' -data='tuple path'


