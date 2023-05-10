import random
import argparse
import sys
import pandas as pd
import csv


parser = argparse.ArgumentParser(
    description="Tupels Generation"
)
parser.add_argument(
    "-task_name", choices=['concatenation', 'weightedSum']
)
parser.add_argument(
    "-task_num", type=int
)
parser.add_argument(
    "-file_name"
)

def generateConcatenationTuple(file_name, task_num):       
    concatInputDim = []
    concatOutputDim = []
    # concatConcatDim = []

    # concat task 
    concatTaskNum = task_num
    # concatTaskNum = 50
    correctConcatTask = random.randint(concatTaskNum//2, concatTaskNum)
    print("concatenation task number: ", concatTaskNum, "\ncorrect concatenate task number: ", correctConcatTask)


    for task_i in range(correctConcatTask): 
        input_num = random.randint(2, 5)
        dim = random.randint(1, 3) # dimension of input
        concatDim = random.randint(0, dim-1) # dimension for concatenating
        if dim == 1:
            # concatConcatDim.append(('Task{}'.format(str(task_i)), 0))
            random1 = random.randint(0, 10)
            if random1 < 8:
                concatOutputDim.append(('Task{}'.format(str(task_i)), [input_num]))
            else:
                concatOutputDim.append(('Task{}'.format(str(task_i)), [random1]))
            for i in range(input_num):
                concatInputDim.append(('Task{}'.format(str(task_i)), [1]))
        else:
            shape = random.sample(range(1, 20), dim)
            shape[concatDim] = 0
            for i in range(input_num):
                input_dim = shape.copy()
                input_dim[concatDim] = random.randint(1,20)
                shape[concatDim] += input_dim[concatDim]
                concatInputDim.append(('Task{}'.format(str(task_i)), input_dim))
            # concatConcatDim.append(('Task{}'.format(str(task_i)), concatDim))
            concatOutputDim.append(('Task{}'.format(str(task_i)), shape))

    for task_i in range(correctConcatTask, concatTaskNum):
        input_num = random.randint(2, 5)
        for input_i in range(input_num):
            shape = random.sample(range(1, 20), random.randint(2, 5))
            concatInputDim.append(('Task{}'.format(str(task_i)), shape))
        shape = random.sample(range(1, 20), random.randint(2, 5))
        concatOutputDim.append(('Task{}'.format(str(task_i)), shape))
        # concatConcatDim.append(('Task{}'.format(str(task_i)), random.randint(0, 5)))

    inputTupleNum = 0
    outputTupleNum = 0
    with open('{}_concate_input.csv'.format(file_name), 'w') as csvfile:
        writer = csv.writer(csvfile)
        for i in concatInputDim:
            writer.writerow(i)
            inputTupleNum += 1

    with open('{}_concate_output.csv'.format(file_name), 'w') as csvfile:
        writer = csv.writer(csvfile)
        for i in concatOutputDim:
            writer.writerow(i)
            outputTupleNum += 1

    print("Number of input tuples:", inputTupleNum)
    print("Number of output tuples:", outputTupleNum)


def generateWeightedSumTuple(file_name, task_num):
    weightedInputDim = []
    weightedOutputDim = []
    weights = []

    # concat task 
    # weightedTaskNum = 500*1000
    weightedTaskNum = task_num
    correctWeightedTask = random.randint(weightedTaskNum//2, weightedTaskNum)
    print("weighted task number: ", weightedTaskNum, "\ncorrect weightedTaskNum task number: ", correctWeightedTask)


    for task_i in range(weightedTaskNum): 
        input_num = random.randint(2, 5)
        pred_out_dim = 0
        for i in range(input_num):
            input_dim = random.randint(2, 5)
            pred_out_dim += input_dim
            weightedInputDim.append(('Task{}'.format(str(task_i)), [input_dim]))
        
        outputRandom = random.randint(0, 10) # output dim
        if outputRandom < 8: # correct for output dim
            weightedOutputDim.append(('Task{}'.format(str(task_i)), [pred_out_dim]))
        else: # error for output dim
            weightedOutputDim.append(('Task{}'.format(str(task_i)), [random.randint(0, 10)]))

        weightsRandom = random.randint(0, 10) # weights vector
        if weightsRandom < 8: # correct for weights vector
            weights.append(('Task{}'.format(str(task_i)), [i for i in range(input_num)]))
        else: # error for weights vector
            weights.append(('Task{}'.format(str(task_i)), [i for i in range(input_num+2)]))


    inputTupleNum = 0
    outputTupleNum = 0
    weightsTupleNum = 0
    with open('{}_weightedSum_input.csv'.format(file_name), 'w') as csvfile:
        writer = csv.writer(csvfile)
        for i in weightedInputDim:
            writer.writerow(i)
            inputTupleNum += 1

    with open('{}_weightedSum_output.csv'.format(file_name), 'w') as csvfile:
        writer = csv.writer(csvfile)
        for i in weightedOutputDim:
            writer.writerow(i)
            outputTupleNum += 1

    with open('{}_weightedSum_weights.csv'.format(file_name), 'w') as csvfile:
        writer = csv.writer(csvfile)
        for i in weights:
            writer.writerow(i)
            weightsTupleNum += 1

    # print(concatInputDim)
    # print(concatOutputDim)
    # print(concatConcatDim)
    print("Number of input tuples:", inputTupleNum)
    print("Number of output tuples:", outputTupleNum)
    print("Number of weight tuples:", weightsTupleNum)


if __name__ == "__main__":
    args = parser.parse_args()
    task_name = args.task_name
    task_num = args.task_num
    file_name = args.file_name
    
    if task_name == 'concatenation':
        generateConcatenationTuple(file_name, task_num)
    else:
        generateWeightedSumTuple(file_name, task_num)

