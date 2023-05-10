import random
import argparse
import os


parser = argparse.ArgumentParser(
    description="Knowledge Graph Abox generation"
)
parser.add_argument(
    "-pipeline_number", default=1000, type=int
)

parser.add_argument(
    "-file_name"
)

def data(id, data_type, data_dim=0):
    did = id[data_type]
    id[data_type] += 1
    id['dp'] += 1
    
    if data_type == 'singleValue':
        data_def = 'singleValue({}).\n'.format(data_type+str(did))
    if data_type == 'structure':
        data_def = 'structure({}).\n'.format(data_type+str(did))
        id['dp'] += 1
    if data_type == 'array':
        data_def = 'array({}).\n'.format(data_type+str(did))
        id['dp'] += 1

        data_dim_str = ''
        if data_dim==0:
            for i in range(3):
                if data_dim_str=='':
                    data_dim_str=str(random.randint(1, 50))
                else:
                    data_dim_str+=', '+str(random.randint(1, 50))
        else:
            for i in data_dim:
                if data_dim_str=='':
                    data_dim_str=str(i)
                else:
                    data_dim_str+=', '+str(i)
        data_def += 'hasDimension({},[{}]).\n'.format(data_type+str(did), data_dim_str)
        id['dp'] += 1
        
    return data_def


def task(id, task_type, whetherEndTask=False):
    tid = id['task']
    id['task'] += 1
    id['dp'] += 1
    random2 = random.randint(0, 100)
    # task_def = '\n:Task'+str(tid) + ' rdf:type owl:NamedIndividual, :' + task_type
    # task_def = '\ntask(Task{}).\n'.format(str(tid)) 
    if task_type == 'concatenation':
        task_def = '\nconcatenation(task{}).\n'.format(str(tid))
    if task_type == 'weightedSum':
        task_def = '\nweightedSum(task{}).\n'.format(str(tid))  
    if task_type == 'mLTraining':
        task_def = '\nmlTraining(task{}).\n'.format(str(tid)) 
    if task_type == 'mLTesting':
        task_def = '\nmlTesting(task{}).\n'.format(str(tid)) 
    if not whetherEndTask:
        # task_def += ' ;\n\t\t:hasNextTask :Task'+str(tid+1)
        task_def += 'hasNextTask(task{}, task{}).\n'.format(str(tid), str(tid+1))
        id['op'] += 1
    if task_type == 'mLTraining' or task_type == 'mLTesting' or random2<35: 
        data_num = random.randint(1, 4)
        data_def = ''
        for i in range(data_num):
            random1 = random.randint(0, 2)
            if random1 == 0:
                did = id['array']
                task_def += 'hasInput(task{}, array{}).\n'.format(str(tid), str(did))
                id['op'] += 1
                data_def += data(id, 'array')
            elif random1 == 1:
                did = id['singleValue']
                task_def += 'hasInput(task{}, singleValue{}).\n'.format(str(tid), str(did))
                id['op'] += 1
                data_def += data(id, 'singleValue')
            elif random1 == 2:
                did = id['structure']
                task_def += 'hasInput(task{}, structure{}).\n'.format(str(tid), str(did))
                id['op'] += 1
                data_def += data(id, 'structure')
        
        ## error: data dimensions and types don't match
        if task_type == 'concatenation':
            task_def += 'hasConcateDim(task{}, {}).\n'.format(str(tid), str(random.randint(0, 2)))
            id['dp'] += 1
            did = id['array']
            task_def += 'hasOutput(task{}, array{}).\n'.format(str(tid), str(did))
            id['op'] += 1
            data_def += data(id, 'array')

        if task_type == 'weightedSum':
            task_def += 'hasWeightVector(task{}, [{}]).\n'.format(str(tid), str(random.randint(0, 5)) + ',' + str(random.randint(0, 5)))
            id['op'] += 1
            id['dp'] += 1
            did = id['array']
            task_def += 'hasOutput(task{}, array{}).\n'.format(str(tid), str(did)) 
            id['op'] += 1
            data_def += data(id, 'array')
        task_def += '\n' + data_def + '\n'

    elif task_type == 'concatenation': ## concatenation, right
        random3 = random.randint(0, 2)
        data_def = ''
        if random3 == 0: # Array
            aid = id['array']
            task_def += 'hasInput(task{}, array{}).\n'.format(str(tid), str(aid))
            id['op'] += 1
            task_def += 'hasInput(task{}, array{}).\n'.format(str(tid), str(aid+1))
            id['op'] += 1
            task_def += 'hasConcateDim(task{}, {}).\n'.format(str(tid), '0')
            id['dp'] += 1
            task_def += 'hasOutput(task{}, array{}).\n'.format(str(tid), str(aid+2))
            id['op'] += 1
            data_def += data(id, 'array',[3,4])
            data_def += data(id, 'array',[5,4])
            data_def += data(id, 'array',[8,4])
            task_def += '\n' + data_def + '\n'
        else: #SingleValue
            svid = id['singleValue']
            task_def += 'hasInput(task{}, singleValue{}).\n'.format(str(tid), str(svid))
            id['op'] += 1
            task_def += 'hasInput(task{}, singleValue{}).\n'.format(str(tid), str(svid+1))
            id['op'] += 1
            task_def += 'hasConcateDim(task{}, {}).\n'.format(str(tid), '0')
            id['dp'] += 1
            aid = id['array']
            task_def += 'hasOutput(task{}, array{}).\n'.format(str(tid), str(aid))
            id['op'] += 1
            data_def += data(id, 'singleValue')
            data_def += data(id, 'singleValue')
            data_def += data(id, 'array',[2,1])
            task_def += '\n' + data_def + '\n'
            
    else: ##weightedSum, right
        random3 = random.randint(0, 2)
        data_def = ''
        if random3 == 0: # Array
            aid = id['array']
            task_def += 'hasInput(task{}, array{}).\n'.format(str(tid), str(aid))
            id['op'] += 1
            task_def += 'hasInput(task{}, array{}).\n'.format(str(tid), str(aid+1))
            id['op'] += 1
            task_def += 'hasWeightVector(task{}, {}).\n'.format(str(tid), '[3,2]')
            id['dp'] += 1
            id['op'] += 1
            task_def += 'hasOutput(task{}, array{}).\n'.format(str(tid), str(aid+2))
            id['op'] += 1
            data_def += data(id, 'array',[3,4])
            data_def += data(id, 'array',[3,4])
            data_def += data(id, 'array',[3,4])
            task_def += '\n' + data_def + '\n'
        else: #SingleValue
            svid = id['singleValue']
            task_def += 'hasInput(task{}, singleValue{}).\n'.format(str(tid), str(svid))
            id['op'] += 1
            task_def += 'hasInput(task{}, singleValue{}).\n'.format(str(tid), str(svid+1))
            id['op'] += 1
            task_def += 'hasWeightVector(task{}, {}).\n'.format(str(tid), '[3,2]')
            id['op'] += 1
            id['dp'] += 1
            task_def += 'hasOutput(task{}, singleValue{}).\n'.format(str(tid), str(svid+2))
            id['op'] += 1
            data_def += data(id, 'singleValue')
            data_def += data(id, 'singleValue')
            data_def += data(id, 'singleValue')
            task_def += '\n' + data_def + '\n'
    
    # print("tid: ", tid, ", and task: ", task_def)
    return task_def

def pipeline(id):
    pid = id['pipeline']
    tid = id['task']
    id['pipeline'] += 1
    pipeline_def = '\nmlPipeline(pipeline{}).\n'.format(str(pid))
    pipeline_def += 'hasStartTask(pipeline{}, task{}).\n'.format(str(pid), str(tid))
    id['op'] += 1
    string2write = pipeline_def

    task_len = random.randint(2, 5)
    random1 = random.randint(0, 100)
    if random1<60:
        task_def = task(id, 'concatenation')
        string2write += task_def
    elif random1<90:
        task_def = task(id, 'weightedSum') # concatenation & weightedSum isa dataProcessing
        string2write += task_def
    
    for i in range(0,task_len):
        r = random.randint(0, 90)
        if r<40:
            task_def = task(id, 'concatenation')
        elif r<70:
            task_def = task(id, 'weightedSum')
        elif r<80:
            task_def = task(id, 'mLTraining')
        else:
            task_def = task(id, 'mLTesting')
        string2write += task_def
    if random.randint(0, 100)<95:
        task_def = task(id, 'mLTesting', True)
        string2write += task_def
    string2write += '\n'
    
    return string2write


def correct_pipeline(id):
    pid = id['pipeline']
    tid = id['task']
    id['pipeline'] += 1
    pipeline_def = '\nmlPipeline(pipeline{}).\n'.format(str(pid))
    pipeline_def += 'hasStartTask(pipeline{}, task{}).\n'.format(str(pid), str(tid))
    id['op'] += 1
    string2write = pipeline_def

    dp_task_len = random.randint(2, 4)
    for i in range(dp_task_len):
        random1 = random.randint(0, 100)
        if random1<60:
            task_def = task(id, 'concatenation')
            string2write += task_def
        else:
            task_def = task(id, 'weightedSum') # concatenation & weightedSum isa dataProcessing
            string2write += task_def
    
    train_task_len = random.randint(2, 3)
    for i in range(0,train_task_len):
        task_def = task(id, 'mLTraining')
        string2write += task_def

    test_task_len = random.randint(1, 2)
    for i in range(0,test_task_len):
        task_def = task(id, 'mLTesting')
        string2write += task_def
    string2write += '\n'
    
    return string2write

       

if __name__ == "__main__":
    args = parser.parse_args()
    file_name = args.file_name

    if os.path.exists(file_name):
        os.remove(file_name)

    num = args.pipeline_num
    with open(file_name, "a") as output:
        id = {'pipeline':0, 'task':0, 'array':0,'singleValue':0,'structure':0, 'ind': 0, 'op': 0, 'dp': 0}
        pipeline_num = random.randint(1, 1000)
        pipeline_num = num
        for i in range(pipeline_num):
            pipeline_str = pipeline(id)
            # output.write(pipeline_str)
        correct_pipeline_num = num
        for i in range(correct_pipeline_num):
            pipeline_str = correct_pipeline(id)
            # output.write(pipeline_str)
            
        ## print("=============")
        ## print(string2write)
        ## output.write(line)

    id['ind'] = id['pipeline'] + id['task'] + id['array'] + id['singleValue'] + id['structure']
    print('pipeline: {}, task, {}, ind: {}, op: {}, dp: {}'.format(id['pipeline'], id['task'], id['ind'], id['op'],id['dp']))

