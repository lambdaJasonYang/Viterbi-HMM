import numpy as np
states = []
minput = './data/test.pos'
#minput = './data/WSJ_24.pos'
tfile = []
POStable = {'Start':[{},{}],'End':[{},{}]}
with open(minput, 'r') as minput2:
    data = minput2.readlines()
    for i, lines in enumerate(data):
        olines = None
        if(i+1 < len(data)):
            olines = data[i+1]
            olines = olines.strip("\n")
            olines = olines.split("\t")
    
        lines = lines.strip("\n")
        lines = lines.split("\t")
        tfile.append(lines)
        past = 0
        if lines == ['']:
            mpos = 'Start'
            if olines != None:
                
                if olines == ['']:
                    opos = 'End'
                else:
                    opos = olines[1]
                if opos not in POStable[mpos][1]:
                    POStable[mpos][1][opos] = 1
                else:
                    POStable[mpos][1][opos] = POStable[mpos][1][opos] + 1
        
            
        if lines != ['']:

            mword = lines[0]
            mpos = lines[1]
            if mpos not in POStable:
                POStable[mpos] = [{},{}] #likihood,transition
            if mword not in POStable[mpos][0]:
                POStable[mpos][0][mword] = 1
            else:
                POStable[mpos][0][mword] = POStable[mpos][0][mword] + 1
            if olines != None:
                #print(lines)
                #print(olines)
                if olines == ['']:
                    opos = 'End'
                else:
                    opos = olines[1]
                if opos not in POStable[mpos][1]:
                    POStable[mpos][1][opos] = 1
                else:
                    POStable[mpos][1][opos] = POStable[mpos][1][opos] + 1
##ss = "fish sleep".split()
##POStable = {'NN':[{'fish':8 , 'sleep':2},{'VB':8, 'NN':1, 'End':1}] ,
##            'VB':[{'fish':5 , 'sleep':5},{'VB':1, 'NN':2, 'End':7}],
##            'Start':[{},{'VB':2, 'NN':8}],
##            'End':[{},{}]}
ss1 = "the orange is not on the table".split()
POStable1 = {'Start':[{},{'IN':0.2,'JJ':0.6,'DT':0.61,'NN':0.13}],
            'DT':[{'the':0.4,'an':0.05,'a':0.3,'these':0.07},{'NN':0.53,'JJ':0.47}],
            'JJ':[{'angry':0.0005,'blue':0.0011,'perfect':0.003,'orange':0.0015},{'NN':1}],
            'NN':[{'book':0.001,'table':0.0005,'fish':0.0002,'orange':0.00001},{'NN':0.25,'VBZ':0.44,'End':0.31}],
            'IN':[{'of':0.2,'in':0.11,'on':0.1,'before':0.001},{'DT':0.6,'JJ':0.34,'End':0.06}],
            'VBZ':[{'is':0.02,'sees':0.0012,'hates':0.002,'sells':0.004},{'IN':0.12,'DT':0.41,'JJ':0.1,'NN':0.22,'End':0.15}],
            'End':[{},{}]
            }
for i in POStable: #each POS
    emit,trans = POStable[i]
    esum = 0
    tsum = 0
    for j in emit:
        esum += emit[j]
    for k in trans:
        tsum += trans[k]
    for j in emit:
        emit[j] = emit[j]/esum
        #pass
    for k in trans:
        trans[k] = trans[k]/tsum
        #pass
def viterbi(POStable,ss):
    mlab = list(POStable.keys())
    posid = {0:'Start',len(mlab)-1:'End'} #length N
    cc = 1
    for i in range(len(mlab)):
        if mlab[i] != 'Start' and mlab[i] != 'End':
            posid[cc] = mlab[i]
            cc += 1
            
    mmat = np.zeros([len(mlab),len(mlab)])
    mmat[0][0] = 1
    def transit(tfrom,tto,flag):#1 transition,0 emission
        #pos from, myin to
        if tto in POStable[tfrom][flag]:
            return POStable[tfrom][flag][tto]
        return 0

    for i in range(mmat.shape[0]): #i is from
        for j in range(mmat.shape[1]):
            mfrom = posid[i]
            mto = posid[j]
            mmat[i][j] = transit(mfrom,mto,1)

    backpt = np.zeros([len(mlab), len(ss)+1])
    obser = np.zeros([len(mlab), len(ss)])

    empmat = np.zeros([len(mlab),len(ss)+1])


    for i in range(0,len(posid)):
        for j in range(0,len(ss)):
            obser[i][j] = transit(posid[i],ss[j],0)
            
    oovprob = np.amin(obser[np.nonzero(obser)])/10.0
    ini = mmat[0,:] * obser[:,0]
    empmat[:,0] = ini

    for i in range(1,len(ss)):
       
        for j in range(1,len(posid)):
            temp = empmat[j,i-1] * mmat[j,:] * obser[:,i]

            ttt = 0
            arg = 0
            for k in range(len(posid)):
                if max(obser[:,i]) == 0:
                    obser[1:,i] = oovprob
                if ttt < empmat[k,i-1] * mmat[k,j] * obser[j,i] :
                    ttt = empmat[k,i-1] * mmat[k,j] * obser[j,i]
                    print(ttt)
                    arg = k
            empmat[j,i] = ttt
            backpt[j,i] = arg
                #k is the state
                #i is the word

    temp1 = empmat[:,-2]*mmat[:,-1]
    ttt = 0
    arg = 0
    for k in range(len(posid)):
        temp = empmat[k,-2] * mmat[k,-1]
        
        if ttt < temp:
            ttt = temp
            arg = k
        empmat[-1,-1] = ttt
        backpt[-1,-1] = arg
    mout = []
    for i in range(1,backpt.shape[1]):
        aim = np.amax(backpt[:,i])
        mout.append(posid[aim])
        #print(posid[aim],ss[i-1])
    return mout
print(viterbi(POStable1,ss1))
