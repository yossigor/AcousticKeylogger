import json

def console(in_queue,target_name, config):
    json_file_path = target_name.split('.')[0] + '.json'
    output = []
    for idx, pred in iter(in_queue.get, None):
        output.append((idx,pred))
    output.sort(key = lambda (x,y): x);
    f= open(json_file_path,"w+")
    f.write(json.dumps(output))
    f.close() 
    '''
    for i, p in output:
        print "{} - {}".format(i, p)
    '''

    
    
