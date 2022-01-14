# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 21:58:48 2021

@author: atlan
"""
import random
import math

monomer_list = []
shuffled_monomer_list = []
free_monomer_list = []
molecule_list = []   
    
initiator_list = []
crosslinker_list = []
TTC_list = []
TFK_list = []
chain_list = []
    
j = 0



current_parameters = {
    'repeats' : 10,
    'conversion' : 0.8,

    'Repeat_unit_length' : 2,
    'crosslinker_length' : 16,
    'TTC_length' : 2,
    'TFK_TTC_length' : 2,
    'TFK_arm_length' : 7,

    'monomer_number' : 10000,
    'crosslinker_number' : 4000,
    'TTC_number' : 0,
    'TFK_number' : 0,
    'initiator_number' : 10,

    'k_transfer_to_ttc' : 20,
    'k_transfer_to_TFK' : 20,
    
    'r1' : 1,
    'r2' : 1
     }

batch_exprmnts = [
        
    {
    'monomer_number' : 1500,
    'crosslinker_number' : 375,
    'TTC_number' : 0,
    'TFK_number' : 125,
    'initiator_number' : 62,
    'r1' : 1,
    'r2' : 1
     },
    
    {
    'monomer_number' : 1500,
    'crosslinker_number' : 375,
    'TTC_number' : 0,
    'TFK_number' : 125,
    'initiator_number' : 62,
    'r1' : 1,
    'r2' : 1
     },

     ]
    
    
     
def batch_init(exprmnt, current_dict):
    global repeats
    global conversion
    global Repeat_unit_length
    global crosslinker_length
    global TTC_length         
    global TFK_TTC_length     
    global TFK_arm_length     
        
    global monomer_number
    global crosslinker_number    
    global TTC_number         
    global TFK_number         
    global initiator_number   
        
    global k_transfer_to_ttc  
    global k_transfer_to_TFK  

    global r1
    global r2
    
    for key in current_parameters:
        if key in exprmnt:
            current_parameters[key] = exprmnt[key]
            
    repeats            = current_dict['repeats']
                    
    conversion         = current_dict['conversion']
        
    Repeat_unit_length = current_dict['Repeat_unit_length']
    crosslinker_length = current_dict['crosslinker_length']
    TTC_length         = current_dict['TTC_length']
    TFK_TTC_length     = current_dict['TFK_TTC_length']
    TFK_arm_length     = current_dict['TFK_arm_length']
        
    monomer_number     = current_dict['monomer_number']
    crosslinker_number = current_dict['crosslinker_number']
    TTC_number         = current_dict['TTC_number']
    TFK_number         = current_dict['TFK_number']
    initiator_number   = current_dict['initiator_number']
            
    k_transfer_to_ttc  = current_dict['k_transfer_to_ttc']
    k_transfer_to_TFK  = current_dict['k_transfer_to_TFK']
    
    r1                  = current_dict['r1']
    r2                  = current_dict['r2']
    
    monomer = monomer_number - crosslinker_number * 2 - TFK_number * 2
    
    print('monomer = ', monomer)
    print('crosslinker = ', crosslinker_number)
    print('TTC = ', TTC_number)
    print('TFK = ', TFK_number)
    print('initiator = ', initiator_number)
    print('r1 = ', r1)
    print('r2 = ', r2)
            
            

class chain:
    
    def __init__ (self, head, tail, head_type = None):
        self.kind = 'chain' #both 'type' and 'id' are reserved...
        self.component = []
        self.head = head
        self.tail = tail
        self.head_type = head_type
            
    def activate(self):
        self.tail = 'radical'
        
    def dormant(self, new_tail):
        self.tail = new_tail
        
class TTC:
    def __init__ (self, chain1, chain2, flank1 = 0, flank2 = 0, elastic = 0):
        self.kind = 'ttc'
        self.chain1 = chain1
        self.chain2 = chain2
        self.flank1 = flank1
        self.flank2 = flank2
        self.elastic = elastic

class TFK:
    def __init__ (self, chain1, chain2, monomer1, monomer2, flank1 = 0, flank2 = 0, elastic = 0):
        self.kind = 'TFK'
        self.chain1 = chain1
        self.chain2 = chain2
        self.monomer1 = monomer1
        self.monomer2 = monomer2
        self.flank1 = flank1
        self.flank2 = flank2
        self.elastic = elastic
        
class crosslinker:
    def __init__ (self, monomer1,monomer2, elastic = None):
        self.kind = 'crosslinker'
        self.monomer1 = monomer1
        self.monomer2 = monomer2
        self.elastic = elastic
        
class monomer:
    def __init__(self, kind, free = True, parent = None, chain = None): #"type" can be used to denote different kinds of polymerizable groups, e.g. acrylate/styrene copolymerization
        self.kind = kind
        self.free = free
        self.parent = parent
        self.chain = chain


def initiation():
    
    monomer_list.clear()
    shuffled_monomer_list.clear()
    free_monomer_list.clear()
    
    
    initiator_list.clear()
    crosslinker_list.clear()
    TTC_list.clear()
    TFK_list.clear()
    chain_list.clear()
    
    
    j = 0

    for i in range(initiator_number):
        initiator_list.append(i)
        
    for i in range(TTC_number):
        TTC_list.append(TTC(None,None))
    
    
    for i in range(monomer_number):
        monomer_list.append(monomer(kind = 1, free = True))
    
    
    j = 0
    
    
    for i in range(crosslinker_number):
        crosslinker_list.append(crosslinker(monomer_list[j],monomer_list[j+1]))
        monomer_list[j].parent = crosslinker_list[i]
        monomer_list[j+1].parent = crosslinker_list[i]
        j += 2
    
    for i in range(TFK_number):
        TFK_list.append(TFK(None, None, monomer_list[j], monomer_list[j+1]))
        monomer_list[j].parent = TFK_list[i]
        monomer_list[j+1].parent = TFK_list[i]
        j += 2
    
    
    j = 0
    
    for trithiocarbonate in TTC_list:
         chain_list.append(chain(head=None, tail=trithiocarbonate))
         chain_list.append(chain(head=None, tail=trithiocarbonate))
         trithiocarbonate.chain1 = chain_list[j]
         trithiocarbonate.chain2 = chain_list[j+1]
         j += 2
         
    for iniferinker in TFK_list:
         chain_list.append(chain(head=iniferinker.monomer1, tail=iniferinker, head_type = 'monomer'))
         chain_list.append(chain(head=iniferinker.monomer2, tail=iniferinker, head_type = 'monomer'))
         iniferinker.monomer1.parent = chain_list[j]
         iniferinker.monomer2.parent = chain_list[j+1]
         iniferinker.chain1 = chain_list[j]
         iniferinker.chain2 = chain_list[j+1]
         iniferinker.monomer1.kind = 2
         iniferinker.monomer2.kind = 2
         j += 2


    for initiator in initiator_list:
         chain_list.append(chain(head=None,tail='radical'))
         #print(chain_list[-1].head)
 
# =============================================================================
#     for xlinker in crosslinker_list:
#         xlinker.monomer1.kind = 2
#         xlinker.monomer2.kind = 2
# =============================================================================

def chain_transfer(chain, CTA_list):
 
     TTC = random.choice(CTA_list)
     chain.dormant(new_tail = TTC)
     TTC_side = random.choice([1,2])
     if TTC_side == 1:
         TTC.chain1.activate()
         TTC.chain1 = chain
     else:
         TTC.chain2.activate()
         TTC.chain2 = chain


def terminate(chain):
    chain.dormant(new_tail = 'terminate')


def chain_grow_alt(chain, counter):
    
    weights = [k_transfer_to_ttc * TTC_number, k_transfer_to_TFK * TFK_number, monomer_number - j]
    switch = random.choices(['transfer_ttc','transfer_TFK','propagate'], weights = weights)
    
    if switch == ['transfer_ttc']:
        chain_transfer(chain, TTC_list)
        return 0
        
    elif switch == ['transfer_TFK']:
        chain_transfer(chain, TFK_list)
        return 0
    
    elif switch == ['terminate']:
        terminate(chain)
        return -1
    
    else:
        new_monomer = random.choice(monomer_list)
        while new_monomer.free == False:
            new_monomer = random.choice(monomer_list)
        chain.component.append(new_monomer)
        new_monomer.free = False
        new_monomer.chain = chain
        return 1
    
    
def chain_grow(chain):
    
    weights = []
    
    for molecule in molecule_list:
        if molecule.kind == 'ttc':
            weights.append(k_transfer_to_ttc)
        elif molecule.kind == 'TFK':
            weights.append(k_transfer_to_TFK)
        elif molecule.kind == 1:
            if len(chain.component) == 0:
                weights.append(1)
            elif chain.component[-1].kind == 1:
                weights.append(1)
            elif chain.component[-1].kind == 2:
                weights.append(1/r1)
        elif molecule.kind == 2:
            if len(chain.component) == 0:
                weights.append(1)
            elif chain.component[-1].kind == 1:
                weights.append(1/r2)
            elif chain.component[-1].kind == 2:
                weights.append(1)
        else:
            print('Molecule reactivity not defined')
    
    reacted = random.choices(molecule_list, weights = weights)
    reacted = reacted[0]

    if reacted.kind == 'ttc' or reacted.kind == 'TFK':
        chain.dormant(new_tail = reacted)
        TTC_side = random.choice([1,2])
        if TTC_side == 1:
            reacted.chain1.activate()
            reacted.chain1 = chain
        else:
            reacted.chain2.activate()
            reacted.chain2 = chain
        return 0
    
    elif reacted.kind == 1 or reacted.kind ==2:
        chain.component.append(reacted)
        reacted.free = False
        reacted.chain = chain
        molecule_list.remove(reacted)
        return 1
    else:
        print('Molecule reactivity not defined')
        
        
def simulation():
    
    molecule_list.clear()
    
    for monomer in monomer_list:
        molecule_list.append(monomer)
        
    for TFK in TFK_list:
        molecule_list.append(TFK)
    
    for TTC in TTC_list:
        molecule_list.append(TTC)
        
    j = 0
    live_chains = initiator_number
    
    while (j < monomer_number * conversion) and live_chains > 0: 
        #print(j)

        chain = random.choice(chain_list)
           
        if chain.tail == 'radical':
            grow_outcome = chain_grow(chain)
               
            if grow_outcome == 1:
                    j += 1
                   
            elif grow_outcome == -1:
                    live_chains -= 1
                
    

def MW_Calculator():
    w = 0
    wsq = 0
    n = 0
    for chain in chain_list:
    #    print (len(chain.component))
     #   print (chain.tail)
        if len(chain.component) == 0:
            continue
        w += len(chain.component)
        wsq += len(chain.component)*len(chain.component)
        n += 1
    
    mw = wsq/w
    mn = w/n
    print (mw, mn, mw/mn)
    print(len(chain_list))
    return mw/mn

def dict_write(master_dict, new_dict):
    for key in new_dict:
        if key in master_dict:
            master_dict[key] += new_dict[key]
        else:
            master_dict[key] = new_dict[key]
            

def MW_btw_Xlink_Calc(crosslinker, TFK, TTC, monomer):
    MW_btw_Xlink = {}
     
        
    for crosslinker in crosslinker_list:
        if crosslinker.monomer1.free == True or crosslinker.monomer2.free == True:
            
            crosslinker.elastic = False
            continue
        buffer = crosslinker_length
        dict_write(MW_btw_Xlink,{buffer:1})
        
   
    for chain in chain_list:
        
        elastic_active = False
        buffer = 0
        
        if chain.head_type == 'monomer' and chain.head.free == False:
            elastic_active = True
            buffer += TFK_arm_length
        
        for monomer in chain.component:
           
            buffer += Repeat_unit_length
            
            if monomer.parent == None:
                
                continue
            
    
            
            elif elastic_active == True:
                
                dict_write(MW_btw_Xlink,{buffer:1})
                buffer = 0

            else:
                
                elastic_active = True
                buffer = 0
        
        if type(chain.tail) == TFK:
            chain.tail.flank1 += buffer
            if elastic_active == False:
                chain.tail.elastic = -1
                        
        elif type(chain.tail) == TTC:
            chain.tail.flank1 += buffer
            if elastic_active == False:
                chain.tail.elastic = -1

    for TFK in TFK_list:
        if TFK.elastic == -1 :
            continue
        
        buffer = TFK_TTC_length + TFK.flank1 + TFK.flank2

        dict_write(MW_btw_Xlink,{buffer:1})   
        
    for TTC in TTC_list:
        if TTC.elastic == -1 :

            continue
        
        buffer = TTC_length + TTC.flank1 + TTC.flank2
        dict_write(MW_btw_Xlink,{buffer:1})
            
    return MW_btw_Xlink


def Avg_XL_per_Chain():
    xlink_number_by_mw = 0
    chain_number = 0
    monomer_number = 0
    print('chain number', len(chain_list))
    for chain in chain_list:   
        
        chain_xlink_number = 0
        chain_monomer_number = 0
        
        if len(chain.component) == 0:
            continue    
        
        if chain.head != None:
            
            if chain.head.free == False:
                chain_xlink_number += 1
        
        if type(chain.tail) == TFK:
            
            if chain.tail.chain1 == chain:
                other_chain = chain.tail.chain2
            else: 
                other_chain = chain.tail.chain1
            
            if other_chain.head != None:
                if other_chain.head.free == False:
                    chain_xlink_number += 1
            
            elif len(other_chain.component) > 0:
                chain_xlink_number += 1
        
        for monomer in chain.component:
         
            chain_monomer_number += 1

            if monomer.parent != None:
                chain_xlink_number += 1
                
        chain_number += 1
        
        xlink_number_by_mw += chain_xlink_number
        monomer_number += len(chain.component)
    
    return {"xlink_number_by_mw":xlink_number_by_mw, "monomer_number":monomer_number, "chain_number":chain_number}
                
    
    


for exprmnt in batch_exprmnts:
    pdi = 0
    data = {}
    Avg_XL = {"xlink_number_by_mw":0, "monomer_number":0,"chain_number":0}
    batch_init(exprmnt, current_parameters)
    for repeat in range(repeats):
        initiation()

        simulation()
        
        MW_btw_Xlink = MW_btw_Xlink_Calc(crosslinker, TFK, TTC, monomer)
        dict_write(data,MW_btw_Xlink)
        
        dict_write(Avg_XL, Avg_XL_per_Chain())
        #print(Avg_XL, Avg_XL['xlink_number_by_mw']/Avg_XL['chain_number'])
    
    total = 0
    segments = 0
    sqr = 0
    for i in data:
        sqr += data[i] * i * i 
        total += data[i] * i
        segments += data[i]
        
    print('Mn_btw_Xlinks = ' , total/segments)
    print('Mw_btw_Xlinks = ' , sqr/total)
    print("Total Segments = ", segments) 
    print("Total MW = ", total) 
    
    import matplotlib.pylab as plt
    
    lists = sorted(data.items()) # sorted by key, return a list of tuples
    x, y = zip(*lists) # unpack a list of pairs into two tuples
    plt.figure(dpi=300)
    plt.bar(x, y)
    plt.show()
    
    import csv 
  
    filename = str(monomer_number) + ',crosslinker = ' + str(crosslinker_number) + ',TTC = ' + str(TTC_number) + ',TFK = ' + str(TFK_number) + ',initiator = ' + str(initiator_number) + ',r1 = ' + str(r1) + ',r2 = ' + str(r2) + '.csv'

    file = open(filename, 'w+', newline ='') 
  
    with file: 
        write = csv.writer(file) 
        write.writerows([['monomer = ', monomer_number - 2 * (crosslinker_number + TFK_number)],['crosslinker = ', crosslinker_number],['TTC = ', TTC_number],['TFK = ', TFK_number],['initiator = ', initiator_number],['r1 = ', r1],['r2 = ', r2]])
        write.writerows(lists)
    
