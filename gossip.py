import random
import queue

"""
模拟gossip机制传播机制
按不同传播参数统计消息会覆盖多少节点
"""

g_nodes = [i for i in range(10000)] # 所有节点
g_rumors = set()					# 传播者即已收到消息者，节点收到消息会向外传播
g_nums = 10							# 传播数
g_queue = queue.Queue()

def rand_targets(source, nums):
	nodes = []
	for i in g_nodes:
		if i == source:
			continue
		nodes.append(i)
	return random.sample(nodes, nums)

def gossip(source):
	targets = rand_targets(source, g_nums)
	#print(source,'->',targets)
	for i in targets:
		if i in g_rumors:
			continue
		g_rumors.add(i)
		badguy = random.choice(range(10))
		if badguy == 1:
			continue
		gossip(i)

def gossip1():
	while g_queue.qsize()>0:
		source = g_queue.get()
		
		# 自私节点，收到消息后不传播
		# 自私节点占比1%
		badguy = random.choice(range(100))
		if badguy == 1:
			continue
			
		targets = rand_targets(source, g_nums)
		for i in targets:
			if i in g_rumors:
				continue
			g_rumors.add(i)
			g_queue.put(i)

if __name__ == '__main__':
	g_rumors.add(g_nodes[0])
	g_queue.put(g_nodes[0])
	# gossip(g_nodes[0])
	gossip1()
	print(len(g_nodes),len(g_rumors))
