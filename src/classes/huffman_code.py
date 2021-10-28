#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Description """

import math
from scipy.stats import entropy

p_dict = {}

codeDic1 = {}
codeDic2 = {}

alphabet = {0: 'stop', 1: 'start', 2: 'counter', 3: 'ariza', 4: 'bobin', 5: 'cozgu', 6: 'ayar'}
string = ['stop', 'start', 'counter', 'start', 'counter', 'start', 'stop', 'ariza', 'stop', 'start', 'counter', 'start',
          'counter', 'start', 'counter', 'start', 'counter']
value = [0.263, 0.263, 0.263, 0.053, 0.053, 0.053, 0.053]

# string = ['stop', 'start', 'stop', 'start', 'stop']
# alphabet = {0: 'stop', 1: 'start'}
# value = [0.9, 0.1]

# string = ['stopstop', 'startstart', 'stopstop', 'startstart', 'stopstop']
# alphabet = {0: 'stopstop', 1: 'stopstart', 2: 'startstop', 3: 'startstart'}
# value = [0.01, 0.09, 0.09, 0.81]

# string = ['stop', 'start', 'stop', 'start', 'stop']
# alphabet = {0: 'stop', 1: 'start'}
# value = [0.1, 0.9]

for i in range(len(alphabet)):
    p_dict[alphabet[i]] = value[i]


class TreeNode:
    def __init__(self, key, freq):
        self.key = key
        self.freq = freq
        self.left_child = None
        self.right_child = None
        self.code = ''


def create_note(pn_dict):
    qt = []
    for j in pn_dict.keys():
        qt.append(TreeNode(j, pn_dict[j]))
    qt.sort(key=lambda item: item.freq, reverse=True)
    return qt


def add(q, node_new):
    if len(q) == 0:
        return [node_new]
    else:
        q = q + [node_new]
        q.sort(key=lambda item: item.freq, reverse=True)
    return q


class NodeQueue:
    def __init__(self, pt_dict):
        self.que = create_note(pt_dict)
        self.size = len(self.que)

    def add_node(self, node):
        self.que = add(self.que, node)
        self.size += 1

    def pop_node(self):
        self.size -= 1
        return self.que.pop()


def creat_huffman_tree(node_q):
    while node_q.size != 1:
        node1 = node_q.pop_node()
        node2 = node_q.pop_node()
        r = TreeNode(None, node1.freq + node2.freq)
        r.right_child = node1
        r.left_child = node2
        node_q.add_node(r)
    return node_q.pop_node()


def huffman_code_dic(roof, x):
    if roof:
        huffman_code_dic(roof.left_child, x + '0')
        roof.code += x
        if roof.key:
            codeDic2[roof.code] = roof.key
            codeDic1[roof.key] = roof.code
        huffman_code_dic(roof.right_child, x + '1')


def trans_encode(string):
    global codeDic1
    transcode = ""
    for ii in string:
        transcode += codeDic1[ii]
    return transcode


def trans_decode(string_code):
    global codeDic2
    code = ""
    ans = ""
    for ch in string_code:
        code += ch
        if code in codeDic2:
            ans += codeDic2[code]
            code = ""
    return ans


if __name__ == '__main__':
    t = NodeQueue(p_dict)
    tree = creat_huffman_tree(t)
    huffman_code_dic(tree, '')
    print(codeDic1, codeDic2)

    a = trans_encode(string)
    print(a)
    aa = trans_decode(a)
    print(aa)
    print(len(a))
    print(len(string))
    aver_length = round(len(a) / len(string), 2)
    print('Durchschnittliche Codierungslänge:', aver_length)

    y = 0
    sum = 0
    for x in alphabet:
        z = alphabet[x]
        print(str(len(codeDic1[z])) + ' => ' + str(value[y]))
        sum = sum + (value[y] * len(codeDic1[z]))
        y = y + 1

    print(sum)

    H = entropy(value, base=2)
    print(H)
    # print(aver_length*math.log(3, 2))
    efficienty = round((H/sum) * 100, 2)
    print ('Codierungseffizienz: ' + str(efficienty) + '%')
