import math

def statisticStd(x):
    x = [10.0, 20.0, 30.0, 40.0, 50.0]
    s0 = [0.0]
    s1 = [0.0]
    s2 = [0.0]
    for val in x:
        s0.append(s0[-1] + math.pow(val, 0))
        s1.append(s1[-1] + math.pow(val, 1))
        s2.append(s2[-1] + math.pow(val, 2))

    s0 = s0[1:]
    s1 = s1[1:]
    s2 = s2[1:]
    muArr = [s1[i]/s0[i] for i in range(len(x))]
    stdArr = [math.sqrt((s2[i+1] - s1[i+1]**2/s0[i+1])/s0[i+1]) for i in range(len(x)-1)]
    mu = s1[idx]/s0[idx]
    std = math.sqrt((s2[i+1] - s1[i+1]**2/s0[i+1])/s0[i+1])
    return mu, std

def statisticStd2(x):
    std2 = []
    for i in range(1, len(x)):
        sqrerror = 0.0
        x_mu = [x[j]-mu[i] for j in range(i+1)]
        sqrerror = [val**2 for val in x_mu]
        std2.append(math.sqrt(sum(sqrerror)/(i+1)))
        #std2.append(sum(sqrerror)/(i+1))
        #std2.append(sum(sqrerror))

    print std2
