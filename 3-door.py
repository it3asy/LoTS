import random
wins = 0
switch = 0 # switch or not
for i in range(100):
	print('round %s' % i)
	car = random.choice(range(3))
	
	# 选择的门
	choice = random.choice(range(3))
	print(' door %s chose' % choice)

	# 打开的门
	for i in range(3):
		if i not in (car,choice):
			open = i
			print(' door %s open[sheep]' % open)
			break
			
	# 留下的门
	left, = [i for i in range(3) if i not in (choice,open)]
	print(' door %s left' % left)
	
	if switch: choice = left 
	if choice == car: wins += 1

print('%s wins' % wins)
