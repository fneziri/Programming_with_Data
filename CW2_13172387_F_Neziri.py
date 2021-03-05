import random as random
import matplotlib.pyplot as plt
import time

'Phase 1: MyHealthcare device: Vital signs simulator'

def myHealthcare(n):
    random.seed(109)
    ts = 0
    data = []
    
    for i in range(0, n):
        ts += 1
        temp = random.randint(36,39)
        hr = random.randint(55,100)
        pulse = random.randint(55,100)
        bloodpr = random.randint(120,121)
        resrate = random.randint(11,17)
        oxsat = random.randint(93,100)
        ph = round(random.uniform(7.1,7.6),1)
        record = [ts, temp, hr, pulse, bloodpr, resrate, oxsat, ph]
        data.append(record)

    return data


'Phase 2: Run analytics'

def abnormalPulseAnalytics(data, sample_size):
    sample = random.sample(data, sample_size) #create a random sample
    count = 0
    values = []
    
    for i in range(0,len(sample)):
        if sample[i][3] == 100 or sample[i][3] < 60:
            count += 1
            values.append([sample[i][0],sample[i][3]])
        else:
            pass
            
    #[i][3] is the index of pulse in each record list
    #100 and < 60 are the abnormal values
    #we can adapt this function for a different vital sign
    #by changing [i][3] to to the index of the vital sign we are interested in
    #and by changing 100 and 60 to the abnormal values of the vital sign
    #we are interested in
        
    output = ['pulse', count, values]
    return output
        
    
def frequencyAnalytics(data, sample_size):
    sample = random.sample(data, sample_size) #create a random sample
    pulses = []
    frequency = []
    
    for i in range(0,len(sample)):
        pulses.append(sample[i][3])
        
    for item in pulses:
        frequency.append([item, pulses.count(item)])

    #remove duplicate lists:
    frequency_list = []
    [frequency_list.append(x) for x in frequency if x not in frequency_list]

    return frequency_list
        

def plotAbnormalPulse(output):
    pairs = sorted(output[2])

    plt.xlabel('Timestamp')
    plt.ylabel('Pulse rate')
    plt.title('Abnormal pulse rates from a random sample of My Healthcare data')
    
    for i in range(0, len(pairs)):
        plt.scatter(pairs[i][0], pairs[i][1], color = 'red')
        plt.annotate(pairs[i], xy = (pairs[i][0], pairs[i][1]))
                     
    plt.show()
    

def plotFrequency(frequency_list):
    frequency_sort = sorted(frequency_list)
    pulse = []
    pulse_frequency = []
    
    for i in range(0, len(frequency_sort)):
        pulse.append(frequency_sort[i][0])
        pulse_frequency.append(frequency_sort[i][1])

    plt.bar(range(len(frequency_sort)), pulse_frequency, align='center')
    plt.xlabel('Pulse')
    plt.ylabel('Frequency')
    plt.title('Frequency histogram of pulse rates')
    plt.xticks(range(len(frequency_sort)), pulse)
    plt.show()


'Phase 3: Search for heart rates using the HealthAnalyzer (pulse value = 56)'

def healthAnalyzerLin(data,key):
    lin_search_output = []

    for i in range(0, len(data)):
        if data[i][3] == key:
            lin_search_output.append(data[i])

    return lin_search_output            
        

def healthAnalyzerBinLower(data, low, high, key):
    data_sort = sorted(data, key = lambda x: x[3])#sort by pulse
    lower_bound = 0
    #lower_bound is used to keep track of the lowest position in the list
    #where our value is found

    while low <= high: 
        mid = low + (high - low) // 2; 

        if data_sort[mid][3] == key: 
            lower_bound = mid
            high = mid - 1
            #we keep searching left to find the first occurence/lower bound
            #as our data contains multiple records with the same pulse
        elif data_sort[mid][3] < key: 
            low = mid + 1
        else: 
            high = mid - 1
    
    return lower_bound


def healthAnalyzerBinUpper(data, low, high, key):
    data_sort = sorted(data, key = lambda x: x[3])#sort by pulse
    upper_bound = 0
    #upper_bound is used to keep track of the highest position in the list
    #where our value is found
    
    while low <= high: 
        mid = low + (high - low) // 2; 
          
        if data_sort[mid][3] == key: 
            upper_bound = mid
            low = mid + 1
            #we keep searching right to find the last occurence/upper bound
            #as our data contains multiple records with the same pulse
        elif data_sort[mid][3] < key: 
            low = mid + 1
        else: 
            high = mid - 1

    return upper_bound


def healthAnalyzerBin(data, low, high, key):
    data_sort = sorted(data, key = lambda x: x[3])#sort by pulse
    bin_search_list = []
    
    lower_bound_index = healthAnalyzerBinLower(data_sort, low, high, key)
    upper_bound_index = healthAnalyzerBinUpper(data_sort, low, high, key)
    
    for i in range(lower_bound_index, upper_bound_index + 1):
        bin_search_list.append(data_sort[i])

    return bin_search_list


def plotHeartPulse(data, pulse):
    
    #use binary search function
    #to find subset of values equal to the pulse value we are looking at
    #use pulse instead of '56'
    #so that the function works for all pulse values
    
    subset = healthAnalyzerBin(data, 0, len(data), pulse)
    
    plt.xlabel('Timestamp')
    plt.ylabel('Heart rate')
    plt.title('Heart rates for pulse of ' +str(pulse))

    for i in range(0, len(subset)):
        plt.scatter(subset[i][0], subset[i][2],color = 'green')
        plt.annotate(subset[i][2], xy = (subset[i][0], subset[i][2])) 
                 
    plt.show()


'Phase 4: Testing scalability of your algorithm'

def benchmarkPhase1(*args):
    #use *args so that the function can be benchamrked for any number of n
    args = list(args)
    time_list = []
    
    for arg in args:
        start = time.time()
        value = myHealthcare(arg)
        end = time.time()
        elapsed_time = (end - start)
        time_list.append(elapsed_time)
        
    pairs = list(zip(args, time_list))

    return pairs

    
def benchmarkPhase2a(sample_size, *args):
    #use *args so that the function can be benchamrked for any number of n
    #use sample_size so function can be used for any sample size specified
    args = list(args)
    time_list = []

    for arg in args:
        start = time.time()
        value = abnormalPulseAnalytics(myHealthcare(arg), sample_size)
        end = time.time()
        elapsed_time = (end - start)
        time_list.append(elapsed_time)
        
    pairs = list(zip(args, time_list))

    return pairs

    
def benchmarkPhase2b(sample_size, *args):
    #use *args so that the function can be benchamrked for any number of n
    #use sample_size so function can be used for any sample size specified
    args = list(args)
    time_list = []

    for arg in args:
        start = time.time()
        value = frequencyAnalytics(myHealthcare(arg), sample_size)
        end = time.time()
        elapsed_time = (end - start)
        time_list.append(elapsed_time)
        
    pairs = list(zip(args, time_list))

    return pairs

    
def benchmarkPhase3Lin(key, *args):
    #use *args so that the function can be benchamrked for any number of n
    #use key so function can be used for any value specified
    args = list(args)
    time_list = []

    for arg in args:
        start = time.time()
        value = healthAnalyzerLin(myHealthcare(arg),key)
        end = time.time()
        elapsed_time = (end - start)
        time_list.append(elapsed_time)
        
    pairs = list(zip(args, time_list))

    return pairs


def benchmarkPhase3Bin(key, *args):
    #use *args so that the function can be benchamrked for any number of n
    #use key so function can be used for any value specified
    args = list(args)
    time_list = []

    for arg in args:
        start = time.time()
        value = healthAnalyzerBin(myHealthcare(arg),0,arg,key)
        end = time.time()
        elapsed_time = (end - start)
        time_list.append(elapsed_time)
    
    pairs = list(zip(args, time_list))

    return pairs

def plotBenchmarkFunction(benchmark_function):
    #benchmark_function relates to the functions created above
    n = [i for i,j in benchmark_function]
    time_list = [j for i,j in benchmark_function]
    
    plt.plot(n, time_list)
    plt.xlabel('# of records')
    plt.ylabel('Time elapsed')
    plt.title('Benchmarking analysis for different data sizes')
    plt.show()


def main():
    print('Phase 1: MyHealthcare device: Vital signs simulator')
    print('[ts, temp, hr, pulse, bloodpr, resrate, oxsat, ph]\n')
    data = myHealthcare(1000)
    print(data)

    print('\nPhase 2: Run analytics\n')
    print('a) Find abnormal values for pulse\n')
    sample_size = 50
    abnormal_pulse = abnormalPulseAnalytics(data, sample_size)
    print(abnormal_pulse)
    print('\nb) Present a frequency histogram of pulse rates.\n')
    frequency = frequencyAnalytics(data, sample_size)
    print(frequency)

    print('\nPhase 3: Search for heart rates using the HealthAnalyzer \
(pulse value = 56)\n')
    low = 0
    high = 1000
    key = 56
    linear = healthAnalyzerLin(data,key)
    binary = healthAnalyzerBin(data,low,high,key)
    print('Linear Search:\n')
    print(linear)
    print('\nBinary Search\n')
    print(binary)
    
    print('\nPhase 4: Testing scalability of your algorithm\
for n = 1000, 2500, 5000, 7500, 10000\n')
    print('myHealthcare function:\n')
    print(benchmarkPhase1(1000,2500,5000,7500,10000))
    print('\nabnormalPulseAnalytics function:\n')
    print(benchmarkPhase2a(sample_size,1000,2500,5000,7500,10000))
    print('\nfrequencyAnalytics function:\n')
    print(benchmarkPhase2b(sample_size,1000,2500,5000,7500,10000))
    print('\nLinear search algorithm:\n')
    print(benchmarkPhase3Lin(key,1000,2500,5000,7500,10000)) 
    print('\nBinary search algorithm:\n')
    print(benchmarkPhase3Bin(key,1000,2500,5000,7500,10000))

    print('\nComplexities and plots (with discussions) for all phases \
are included in the technical annex\n') 

if __name__ == "__main__": 
    main()
    

