import random

"""
模拟区块链中的51%攻击
攻击者在不同的算力占比(pr_hack)和落后块数(leads)下的成功率
"""

def make_choice(p): #按概率做选择
	x = random.choice(range(100))
	if x< p * 100:
		return True
	return False

def go_hack(leads=6, pr_hack=0.5):
	step = 0
	while True:
		r = make_choice(pr_hack)
		if r == True:
			leads -= 1
		else:
			leads += 1
		if leads >= 1000: # 落后块数过多则认为失败
			return (False, step)
		if leads == 0:	# 追上
			return (True, step)
		step += 1

step_counter = []
tries = 10000   
for i in range(tries):
	ret, steps = go_hack(leads=6, pr_hack=0.5)
	if ret:
		step_counter.append(steps)	
wins = len(step_counter) 		#成功次数
print(float(wins)/float(tries))	#成功率
