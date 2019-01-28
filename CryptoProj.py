import random
import timeit
import time
import numpy as np
import matplotlib.pyplot as plt


'''
                        SELFISH MINING SIMULATION

fraction of hash power owned by selfish miner e.g. alpha = 0.35 Hashrate
fraction of honest miners that build on selfish miner block: 0 <= gamma <= 1 e.g. gamma= 0.25

number of cycles e.g. cycles = 200000

reward for finding a block b = 12.5 BTC

average inter-block validation time (around 10 min for bitcoin) in seconds t_0=600 
'''

def SelfishMining(alpha, gamma, cycles):#(alpha, gamma, cycles)
    start= time.time()  # computing execution time for the algorithm
    
    # -------- initializing values --------------
    t_0=600             # average time (seconds) for mining 1 block
    tm=0                # total time for mining up to now
    tfm=0               # time for mining these 2016 blocks
    ts=0                # time for selfish miner to mine
    hon_bl = 0          # honest block
    hon_or = 0          # honest orphans
    hon = 0             # honest chain
    self_bl = 0         # selfish blocks
    self_or = 0         # selfish orphans
    self = 0            # selfish chain
    beta= 1- alpha      # honest miner hashrate
    bl2016= 0           # blocks mined from 0 to 2016 in this tranche
    nda=0               # number of difficulty adjustments
    diff= 1             # initial difficulty at 1
    b= 12.5             # reward for mining a block
    actual= 20160       # initializing
    Prof_time= 0        # initializing Prof. time for the attacker
                        # i.e. when the attack becomes profitable
                        # for the attacker

    for i in range(1, cycles):
        if (tm != 0.0):
            if (self_bl/(tm/60) > beta):
                Prof_time= tm/60
                
        if (bl2016)>=2015:
            bl2016=0
            nda+=1
            expected= float(2016*(t_0/60))  #time expected for mining 2016 blocks
            actual= tfm                     #actual time for mining this tranche of 2016 blocks
            #tm +=tfm 
            tfm=0
            diff= expected/actual           #difficulty changed

        var= random.random()
        if var < alpha:
        # Selfish miner finds a block
            if self > 0 and self == hon:
                # Selfish miner publishes his blocks to win the competition
                self = self + 1
                self_bl += self
                bl2016 += 1
                a=random.expovariate(1.0/(t_0*diff/60))
                tm+=a
                tfm+= a
                ts += a
                hon_or += hon
                hon = 0
                self = 0
            else:
                # Selfish miner mines selfishly
                if ((self == 0 and hon == 0) or self > hon):
                    self = self + 1
        else:
        # Honest miner finds a block
            if self == 0:
                # HM publishes and SM builds on top
                if hon == 0:
                    hon +=  1
                    hon_bl += hon
                    bl2016 += 1
                    a=random.expovariate(1.0/(t_0*diff/60))
                    tfm+= a
                    tm += a
                    self_or += self
                    hon = 0
                    self = 0
            elif (self == hon and random.random() < gamma):
                # In case of a competition, a percentage gamma of HM build on SM's chain
                # and this gets the longest published chain
                if hon == 1:
                    self_bl += self
                    bl2016 += 1
                    a=random.expovariate(1.0/(t_0*diff/60))
                    tm +=a
                    tfm+= a
                    ts += a
                    hon_or += hon
                    hon = 0
                    self = 0
                    hon_bl += 1
                    bl2016 += 1
            else:
                # HM builds on its own chain.
                hon += 1
                if self == hon + 1:
                    # If SMs chain is longer by exactly 1,
                    # SM will publish his longer chain.
                    self_bl += self
                    bl2016 += self
                    a=random.expovariate(1.0/(t_0*diff/60))
                    tfm+= a
                    tm +=a
                    ts += a
                    hon_or += hon
                    hon = 0
                    self = 0
                elif hon > self:
                    # if HM has longer chain, SM switches to it.
                    hon_bl += hon
                    bl2016 += 1
                    a=random.expovariate(1.0/(t_0*diff/60))
                    tfm+= a
                    tm +=a
                    self_or += self
                    hon = 0
                    self = 0
    end= time.time()
    if diff==1:
        pr= alpha-(1-gamma)*(beta*beta*alpha*(beta-alpha)/(1+beta*alpha)*(beta-alpha)+beta*alpha)*b/(t_0*nda)
        #profitability ratio before adjustment
        ah= alpha-(1-gamma)*beta*beta*alpha*(beta-alpha)/((1+beta*alpha)*(beta-alpha)+beta*alpha)
        #apparent hashrate before adjustment
    else:
        pr= alpha-(1-gamma)*(beta*beta*alpha*(beta-alpha)/(1+beta*alpha)*(beta-alpha)+beta*alpha)*b/(t_0*nda)
        pr= pr * (beta-alpha + beta*alpha*(beta-alpha)+beta*alpha)/(beta*beta*alpha+beta-alpha)
        #profitability ratio after adjustment
        ah= alpha-(1-gamma)*beta*beta*alpha*(beta-alpha)/((1+beta*alpha)*(beta-alpha)+beta*alpha)
        ah= ah*(beta-alpha + beta*alpha*(beta-alpha)+beta*alpha)/(beta*beta*alpha+beta-alpha)

    orphan_ratio= (self_or + hon_or) / float(self_bl + hon_bl + self_or + hon_or)
    apphash_selfish=self_bl/float(self_bl + hon_bl)
    orphan_ratio_honest= hon_or / float(hon_bl + hon_or)
    orphan_ratio_selfish= self_or / float(self_bl + self_or)
    petit_delta= actual/(2016*600)
    delta= 1/petit_delta
    revenue_ratio= apphash_selfish*b/(t_0/60)
    time_spent= tm + tfm
    
    
    concl=[apphash_selfish] #apparent hashrate attacker
    concl.append(ah)                        #theoretical apparent hashrate
    concl.append(orphan_ratio)
    concl.append(nda)
    concl.append(petit_delta)
    concl.append(revenue_ratio)
    concl.append(time_spent/(60*24*7))
    concl.append(self_bl + hon_bl)
    concl.append(Prof_time)
    concl.append(orphan_ratio_honest)
    concl.append(orphan_ratio_selfish)
    return concl

    
def Show():
    
    cycles=2000000
    alpha=0.4
    gamma=0.5

    selfish= SelfishMining(alpha, gamma, cycles)
    print("---------------------------------------------")
    print("Iterations: %d, alpha: %f, gamma: %f\n" % (cycles, alpha, gamma))
    print("Apparent Hashrate attacker: %f " % (selfish[0]))
    print("Orphan ratio: %f" % (selfish[2]))
    print("Orphan ratio honest: %f" % (selfish[9]))
    print("Orphan ratio selfish: %f" % (selfish[10]))
    print("Number of difficulty adjustments: %d" %(selfish[3]))
    print("Theoretical Long-Term apparent hashrate: %f" %(selfish[1]))
    print("Revenue Ratio attacker: %f" %(selfish[5]))
    print("Time spent for mining %d blocks: %f weeks" %(selfish[7],selfish[6]))
    print("Time when an attack becomes profitable: %f weeks" %(selfish[8]/(60*24*7)))
    print("---------------------------------------------")

def Comparison(start,stop,step,alpha,gamma):
    x=[]
    y=[]
    sim=[]
    for i in range(start,stop,step):
        a= SelfishMining(0.4,0.5,i)
        x.append(a[0])
        y.append(a[1])
        sim.append(i)
    return [x,y,sim]

def ShowGraph():
    graph=Comparison(100000,2000000,10000,0.35,0.25)
    plt.plot(graph[2],graph[0])
    plt.plot(graph[2],graph[1])
    plt.ylabel('Comparison')
    plt.show()


def EvolutionGamma():
    x=[]
    sim=[0,0.1, 0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    for i in sim:
        a= SelfishMining(0.35,i,200000)
        x.append(a[0])
    return [x,sim]

def EvolutionAlpha():
    x=[]
    sim=[0,0.05,0.1,0.15, 0.2,0.25,0.3,0.35,0.4,0.45,0.5]
    for i in sim:
        a= SelfishMining(i,0.25,200000)
        x.append(a[0])
    return [x,sim]
  
def ShowGamma():
    graph= EvolutionGamma()
    plt.plot(graph[1], graph[0])
    plt.ylabel('Apparent Hashrate')
    plt.xlabel('Gamma')
    plt.show()

def ShowAlpha():
    graph= EvolutionAlpha()
    plt.plot(graph[1], graph[0])
    plt.ylabel('Apparent Hashrate')
    plt.xlabel('Alpha')
    plt.show()

Show()
#ShowGamma()
#ShowAlpha()
#ShowGraph()
