from dst.libraries.dictionary_filter import dictionary_interactive

#target_1 = ['h','e','l','l','o','_','w','o','r','l','d','_','h','e','l','l','o','_','w','o','r','l','d']
#target_2 = ['U3','U0','U8','U5','U6','U1','U5','U6','U2']
#target_3 = ['o','n','e','_','r','i','n','g','_','t','o','_','r','u','l','e','_'
#            ,'t','h','e','m','_','a','l','l','_','o','n','e','_','r','i','n','g','_','t','o','_'
#           ,'f','i','n','d','_','t','h','e','m','_','o','n','e','_','r','i','n','g','_','t','o','_'
#            ,'b','r','i','n','g','_','t','h','e','m','_','a','l','l','_','a','n','d','_','i','n','_'
#            ,'t','h','e','_','d','a','r','k','n','e','s','s','_','b','i','n','d','_','t','h','e','m']
#target_4 = 'meshithequeenofthismotherfuckingworld'
#target_4 = list(target_4)

#print target_4

def calculateAccuracy(target, top, output):
    count = 0
    for i in range(0,len(target)):
        for j in range(0,top):
            if(output[i][j]==target[i]):
                count += 1
    print(count)
    return float(count)/float(len(target))

def console(in_queue, config):
    #for s_line in config.SPLASHSCREEN:
    #    print s_line
    #print "im output"
    output = []
    for idx, pred in iter(in_queue.get, None):
        output.append((idx,pred))
    output.sort(key = lambda (x,y): x);
    print "PREDICTIONS"
    print ""
    for i, p in output:
        print "{} - {}".format(i, p)
    
    #for top in range(1,6):
    #    print "top_{} accuracy on target_3: {}".format(top,calculateAccuracy(target_3,top,output));
    #dictionary_interactive([y for (x,y) in output], config)

    
    
