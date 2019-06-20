'''
决策树算法 用于建立用户喜好特征

未完成
'''

from math import log
import operator
import treePlotter
import matplotlib.pyplot as plt 
import random
import logging
logging.basicConfig(level = logging.INFO)

# %matplotlib inline


#Input Data
#    数据集有四个特征 'outlook', 'temperature', 'humidity(湿度)', 'windy'， 接下来要计算它们的信息增益率，来选择节点的构成方式。

def createDataSet(dataSet):
    """
    传入数据集:    
    主题-> "文化古迹-0","自然风光-1","展馆-2","公园-3","农家度假-4","游乐场-5","城市观光-6","运动健身-7"
    
    级别-> 0：5A景区 | 1：4A景区 | 2：3A景区 | 3：其他
    
    热度-> 0： 1.0 | 1： 0.7 - 0.99 | 2：0.7以下
    
    地址-> 0：在本省 | 1： 不在本省
    
    价格-> 0：免费 | 1：0.1-50元 起 | 2：50-500元  | 3：500元及以上 | 4：未知

    评分-> 1：极度讨厌 | 2：不怎么滴 | 3：一般般吧 | 4：还可以哦 | 5： 再来一次！
    """
    dataSet = dataSet
    labels = ['theme', 'level_a', 'level_hot', 'address', 'price']
    # outlook->  0: sunny | 1: overcast | 2: rain
    # temperature-> 0: hot | 1: mild | 2: cool
    # humidity-> 0: high | 1: normal
    # windy-> 0: false | 1: true 
    
    # dataSet = [[0, 0, 0, 0, 'N'], 
    #            [0, 0, 0, 1, 'N'], 
    #            [1, 0, 0, 0, 'Y'], 
    #            [2, 1, 0, 0, 'Y'], 
    #            [2, 2, 1, 0, 'Y'], 
    #            [2, 2, 1, 1, 'N'], 
    #            [1, 2, 1, 1, 'Y']]
    # labels = ['outlook', 'temperature', 'humidity', 'windy']
    return dataSet, labels


#计算熵

def calcShannonEnt(dataSet):
    """
    输入：数据集
    输出：数据集的香农熵
    描述：计算给定数据集的香农熵；熵越大，数据集的混乱程度越大
    """
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1      # 数每一类各多少个， {'Y': 4, 'N': 3}
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

def majorityCnt(classList):
    """
    输入：分类类别列表
    输出：子节点的分类
    描述：数据集已经处理了所有属性，但是类标签依然不是唯一的，
          采用多数判决的方法决定该子节点的分类
    """
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reversed=True)
    return sortedClassCount[0][0]


#选择最大的gain ratio对应的feature

def chooseBestFeatureToSplit(dataSet):
    """
    输入：数据集
    输出：最好的划分维度
    描述：选择最好的数据集划分维度
    """
    numFeatures = len(dataSet[0]) - 1                 #feature个数
    baseEntropy = calcShannonEnt(dataSet)             #整个dataset的熵
    bestInfoGainRatio = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]  #每个feature的list
        uniqueVals = set(featList)                      #每个list的唯一值集合                 
        newEntropy = 0.0
        splitInfo = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)  #每个唯一值对应的剩余feature的组成子集
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
            splitInfo += -prob * log(prob, 2)
        infoGain = baseEntropy - newEntropy              #这个feature的infoGain
        if (splitInfo == 0): # fix the overflow bug
            continue
        infoGainRatio = infoGain / splitInfo             #这个feature的infoGainRatio      
        if (infoGainRatio > bestInfoGainRatio):          #选择最大的gain ratio
            bestInfoGainRatio = infoGainRatio
            bestFeature = i                              #选择最大的gain ratio对应的feature
    return bestFeature


#划分数据，为下一层计算准备

def splitDataSet(dataSet, axis, value):
    """
    输入：数据集，选择维度，选择值
    输出：划分数据集
    描述：按照给定特征划分数据集；去除选择维度中等于选择值的项
    """
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:                      #只看当第i列的值＝value时的item
            reduceFeatVec = featVec[:axis]              #featVec的第i列给除去
            reduceFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reduceFeatVec)            
    return retDataSet


#多重字典构建树

def createTree(dataSet, labels):
    """
    输入：数据集，特征标签
    输出：决策树
    描述：递归构建决策树，利用上述的函数
    """
    classList = [example[-1] for example in dataSet]         # ['N', 'N', 'Y', 'Y', 'Y', 'N', 'Y']
    if classList.count(classList[0]) == len(classList):
        # classList所有元素都相等，即类别完全相同，停止划分
        return classList[0]                                  #splitDataSet(dataSet, 0, 0)此时全是N，返回N
    if len(dataSet[0]) == 1:                                 #[0, 0, 0, 0, 'N'] 
        # 遍历完所有特征时返回出现次数最多的
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)             #0－> 2   
        # 选择最大的gain ratio对应的feature
    bestFeatLabel = labels[bestFeat]                         #outlook -> windy     
    myTree = {bestFeatLabel:{}}                   
        #多重字典构建树{'outlook': {0: 'N'
    del(labels[bestFeat])                                    #['temperature', 'humidity', 'windy'] -> ['temperature', 'humidity']        
    featValues = [example[bestFeat] for example in dataSet]  #[0, 0, 1, 2, 2, 2, 1]     
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]                                #['temperature', 'humidity', 'windy']
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
            # 划分数据，为下一层计算准备
    logging.info(print("myTree:", myTree))
    return myTree



#对新数据进行分类

def classify(inputTree, featLabels, testVec):
    """
    输入：决策树，分类标签，测试数据
    输出：决策结果
    描述：跑决策树
    """

    firstStr = list(inputTree.keys())[0]                       # ['outlook'], outlook
    secondDict = inputTree[firstStr]                           # {0: 'N', 1: 'Y', 2: {'windy': {0: 'Y', 1: 'N'}}}
    featIndex = featLabels.index(firstStr)                     # outlook所在的列序号0 
    for key in secondDict.keys():                              # secondDict.keys()＝[0, 1, 2]
        if testVec[featIndex] == key:                          # secondDict[key]＝N
            # test向量的当前feature是哪个值，就走哪个树杈
            if type(secondDict[key]).__name__ == 'dict':       # type(secondDict[key]).__name__＝str
                # 如果secondDict[key]仍然是字典，则继续向下层走
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                # 如果secondDict[key]已经只是分类标签了，则返回这个类别标签
                classLabel = secondDict[key]
        else:
            #没有的默认
            value = random.randint(2,4)
            logging.debug("value: %s",value)
            classLabel = value
    return classLabel

################################################
# Create Test Set  对某用户的对新景点喜好情况进行 预测
def createTestSet():
    # testSet = [[0, 1, 0, 0], 
    #            [0, 2, 1, 0], 
    #            [2, 1, 1, 0], 
    #            [0, 1, 1, 1], 
    #            [1, 1, 0, 1], 
    #            [1, 0, 1, 0], 
    #            [2, 1, 0, 1]]

    testSet = [[0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0],
                [1, 0, 0, 0, 2],
                [2, 1, 0, 0, 0],
                [2, 2, 1, 0, 0],
                [2, 2, 1, 1, 0],
                [1, 2, 1, 1, 0]]
    return testSet
#################################################


#对多条新数据进行分类

def classifyAll(inputTree, featLabels, testDataSet):
    """
    输入：决策树，分类标签，测试数据集
    输出：决策结果
    描述：跑决策树
    """
    classLabelAll = []
    for testVec in testDataSet:               #逐个item进行分类判断
        classLabelAll.append(classify(inputTree, featLabels, testVec))
    return classLabelAll

def get_a_dataSet(dataSet_default1):
    '''
    传入数据集
    '''
    """ if dataSet_now = None :
        dataSet_now = [[0, 0, 0, 0, 0,1],
                [0, 0, 0, 1, 0,1]] """
    ##############################
    #等待传入数据集
    ##################################
    dataSet_default2 = dataSet_default1
    dataSet_default = [[0, 0, 0, 1, 2,"5"],
                                [0, 3, 2, 1, 1,"3"],
                                [2, 3, 2, 1, 2,"4"],
                                [2, 3, 1, 1, 0,"5"],
                                [7, 3, 2, 0, 2,"2"],
                                [0, 3, 0, 1, 1,"5"],
                                [1, 1, 1, 1, 2,"3"],
                                [1, 1, 2, 1, 2,"3"],
                                [3, 3, 1, 1, 2,"4"],
                                [5, 3, 2, 1, 2,"3"]]
    return dataSet_default2

#创建用户初始喜好情况
#可视化决策树的结果

#dataSet_now = get_a_dataSet()

#dataSet, labels = createDataSet(dataSet_now)
#labels_tmp = labels[:]
#desicionTree = createTree(dataSet, labels_tmp)
#treePlotter.createPlot(desicionTree) 可视化决策树


# inputTree = desicionTree
# featLabels = ['theme', 'level_a', 'level_hot', 'address', 'price']
# testVec = [1, 1, 1, 1, 1]
# classify(inputTree, featLabels, testVec)


# #对新景点 喜好情况 预测
# testSet = createTestSet()
# print('classifyResult:\n', classifyAll(desicionTree, labels, testSet))
