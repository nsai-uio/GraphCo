import random
import argparse
import sys
from pyspark.sql import SparkSession
import time
import findspark
import csv
import pandas as pd

findspark.init()
findspark.find()
spark = SparkSession.builder.appName('kgVerify').getOrCreate()

parser = argparse.ArgumentParser(
    description="Knowledge Graph Verify"
)
parser.add_argument(
    "-exp", default=4, type=int, choices=[4, 5, 6],
    help="experiment"
)
parser.add_argument(
    "-data", help="number of tasks"
)

       

def experiment4(data):
    # running time in pyspark
    data = '{}_concate_input.csv'.format(data)

    rdd_concatInput=spark.read.csv(data).rdd

    start_time = time.time()

    rdd_inputDimNoMatch = rdd_concatInput.mapValues(lambda value: len(value.split(','))).groupByKey().filter(lambda x: len(set(x[1]))!=1)

    verify_result = rdd_inputDimNoMatch.first()

    end_time = time.time()
    running_time = end_time - start_time
    print("pyspark running time: ", running_time)   

    # running time in python
    concatInputDim = pd.read_csv(data, header=None)
    start_time = time.time()
    concat_input_dimension_dict = {}
    false_task_exp4 = []

    for index, i in concatInputDim.iterrows():
        if i[0] not in concat_input_dimension_dict:
            concat_input_dimension_dict[i[0]] = [len(i[1].split(','))]
        else:
            concat_input_dimension_dict[i[0]].append(len(i[1].split(',')))

    for i in concat_input_dimension_dict:
        tmp = len(set(concat_input_dimension_dict[i]))
        if tmp != 1:
            false_task_exp4.append(i)
    x = false_task_exp4[0]     
    end_time = time.time()
    running_time = end_time - start_time
    print("python running time: ", running_time)    


def experiment5(data):    
    weightedInput_path = '{}_weightedSum_input.csv'.format(data)
    weightedWeights_path = '{}_weightedSum_weights.csv'.format(data)

    rdd_weightedInput=spark.read.csv(weightedInput_path).rdd
    rdd_weights=spark.read.csv(weightedWeights_path).rdd

    start_time = time.time()

    rdd_weightsInputNum = rdd_weightedInput.mapValues(lambda value: 1).reduceByKey(lambda a,b : a+b)

    rdd_weightsNoMatch = rdd_weights.mapValues(lambda value: len(value.split(','))).join(rdd_weightsInputNum).filter(lambda x: x[1][0]>x[1][1])

                            #[("task1", [3,4])] false, [("task1", [3])] true
    verify_result = rdd_weightsNoMatch.first()

    end_time = time.time()
    running_time = end_time - start_time
    print("pyspark running time: ", running_time)   

    # running time in python
    input_results = pd.read_csv(weightedInput_path, header=None)
    weights_results = pd.read_csv(weightedWeights_path, header=None)


    start_time = time.time()

    input_num = {}
    false_task = []

    for index, i in input_results.iterrows():
        if i[0] not in input_num:
            input_num[i[0]] = 1
        else:
            input_num[i[0]] += 1

    for index, i in weights_results.iterrows():
        if len(i[1]) > input_num[i[0]]:
            false_task.append(i[0])
    task = false_task[0]

    end_time = time.time()
    running_time = end_time - start_time
    print("python running time: ", running_time)   



def experiment6(data):
    weightedInput_path = '{}_weightedSum_input.csv'.format(data)
    weightedOutput_path = '{}_weightedSum_output.csv'.format(data)
   
    # running time in pyspark
    rdd_weightedInput=spark.read.csv(weightedInput_path).rdd
    rdd_weightedOutput=spark.read.csv(weightedOutput_path).rdd

    start_time = time.time()

    rdd_verify = rdd_weightedInput.reduceByKey(lambda a,b : a+b).join(rdd_weightedOutput).filter(lambda x: x[1][0]!=x[1][1])

                            #[("task1", [3,4])] false, [("task1", [3])] true
    verify_result = rdd_verify.first()

    end_time = time.time()
    running_time = end_time - start_time
    print("pyspark running time: ", running_time)   

    # running time in python
    input_results = pd.read_csv(weightedInput_path, header=None)
    output_results = pd.read_csv(weightedOutput_path, header=None)

    start_time = time.time()

    pred_out = {}
    false_task = []

    for index, i in input_results.iterrows():
        if i[0] not in pred_out:
            pred_out[i[0]] = i[1]
        else:
            pred_out[i[0]] += i[1]

    for index, i in output_results.iterrows():
        if i[1] != pred_out[i[0]]:
            false_task.append(i[0])
    task = false_task[0]

    end_time = time.time()
    running_time = end_time - start_time
    print("python running time: ", running_time)    



if __name__ == "__main__":
    args = parser.parse_args()
    # data = generateRadomData(args.exp, args.task)
    if args.exp == 4:
        experiment4(args.data)
    elif args.exp == 5:
        experiment5(args.data)
    elif args.exp == 6:
        experiment6(args.data)

spark.stop()
