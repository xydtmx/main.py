import random

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import networkx as nx
import matplotlib.pyplot as plt
#from matplotlib import pyplot as plt
import numpy as np
#from numpy import *

class message:
    def __init__(self):
        self.route = []
        self.length = 1
        self.if_used = 0  #在这次循环内是否被转发过

class node:
    def __init__(self):
        self.neighbour = []   #相邻节点编号
        self.queue = []  #正在排队消息数
        self.capacity = 30  #节点容量
        self.message_in_queue = []   #队列内消息详细


def message_creat(n):
    sourse = random.randint(0,n-1)  #随机生成源节点序号
    target = random.randint(0,n-1)
    while target == sourse :
        target = random.randint(0,n-1)   #随机生成不重复的目标节点序号
    s = message()
    s.route = nx.shortest_path(G1,sourse,target)  #最短路径路由
    return s



n=100  #节点数
k=5
p=0.6
G=nx.watts_strogatz_graph(n, k, p)

G1 = nx.DiGraph()
G1 = G.to_directed()

#print(G1)


#G = nx.random_graphs.erdos_renyi_graph(50,0.2)
#pos = nx.shell_layout(G)


#G = nx.random_graphs.barabasi_albert_graph(50,1)
#pos = nx.spring_layout(G)

#print(G.edges)
#print(G.nodes)
#print(list(G.neighbors(0)))  # 其中的34为所要求目标节点


net = []  #网络list
for i in range(n):
    net.append(node())   #生成网络节点
    net[i].neighbour = list(G1.neighbors(i))
    #print(len(net[i].neighbour))
    net[i].capacity = 20    #
    for j_node in range(len(net[i].neighbour)):
        net[i].queue.append(0)   #当前节点当前队列长度
        net[i].message_in_queue.append([])  #消息队列第一位置为下一节点编号
        net[i].message_in_queue[j_node].append(net[i].neighbour[j_node])
print(net[1].message_in_queue)





for i in range(1000):
    counter = 0
    for i_message in range(30):  # 一次生成n条信息
        s = message_creat(n)
        #print(s.route)
        source = s.route[0]
        # print(s.route[0])
        for j_message in range(len(net[source].neighbour)):
            if net[source].message_in_queue[j_message][0] == s.route[1]:
                net[source].message_in_queue[j_message].append(s)
                net[source].queue[j_message] += 1

        # print(len(net[source - 1].message_in_queue[0].route))

    for j in range(n):  #对每个节点进行一次操作
        for j_queue in range(len(net[j].neighbour)):#对源节点的每个输出队列进行操作   j_queue是当前节点输出队列总数
            if net[j].queue[j_queue] > 0 and len(net[j].message_in_queue[j_queue][1].route) > 1 and net[j].message_in_queue[j_queue][1].if_used == 0:#如果当前节点输出队列消息数大于一且该消息所处的不是目标节点且该消息未被处理过
                #net[j - 1].message_in_queue[j_queue][0]是该队列下一跳的节点
                del net[j].message_in_queue[j_queue][1].route[0]
                next = net[j].message_in_queue[j_queue][1].route[0]  #next是当前消息的下一跳的节点编号
                for k_queue in range(len(net[next].neighbour)):   #寻找当前消息下一跳所在的输出队列
                    if net[next].message_in_queue[k_queue][0] == net[j].message_in_queue[j_queue][1].route:
                        net[next].message_in_queue[k_queue].append(net[j].message_in_queue[j_queue][1])
                        net[next].message_in_queue[k_queue][-1].if_used = 1
                        net[next].queue[k_queue] += 1
                        if net[next].queue[k_queue] > net[next].capacity:
                            for i_queue in range(len(net[next].neighbour)):
                                G1.add_weighted_edges_from([(next, net[next].neighbour[i_queue], 0)]) #修改拓扑：删除

                del net[j].message_in_queue[j_queue][1]   #删除源节点的信息
                net[j].queue[j_queue] -= 1
            elif net[j].queue[j_queue] > 1 and len(net[j].message_in_queue[j_queue][1].route) == 1 and net[j].message_in_queue[j_queue][1].if_used == 0:#如果当前节点输出队列消息数大于一且该消息所处的是目标节点且该消息未被处理过
                del net[j].message_in_queue[j_queue - 1][1]
                net[j].queue[j_queue] -= 1

    for i_counter in range(n):
        for j_counter in range(len(net[i_counter].neighbour)):
            if net[i_counter].queue[j_counter] > 0:
                net[i_counter].message_in_queue[j_counter][1].if_used = 0   #重置消息的被转发情况
                counter += net[i_counter].queue[j_counter]




        #print(net[k - 1].queue)
    #print(counter)
    #print(i)
    #print("xxxxxxxxxxxxx")








#print(net[0].neighbour)
#print(net[1].neighbour)
#print(net[2].neighbour)
#print(net[3].neighbour)
#print(net[4].neighbour)

nx.draw(G1)
plt.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
