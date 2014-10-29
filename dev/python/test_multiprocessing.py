from multiprocessing import Process, Queue, Pool
import time
import itertools

def f(name, q):
		print 'hello', name
		res=f2(99999)
		q.put([name,res])
		print 'bye ', name

def f2(numiter,power):
		res=0
		for i in range(numiter):
				res=i**power
	   
		return res

def f2_star(numiter_power):
		"""Convert `f([1,2])` to `f(1,2)` call."""
		return f2(*numiter_power)

def f_star(numiter_power_name):
		name = numiter_power_name[-1]
		print 'hello', name
		res = f2_star(numiter_power_name[0:2])
		print 'bye ', name
		return (res, name)

def p_f2(numiter):
		return f2(numiter,power=20)

if __name__ == '__main__':
		if False:
				q = Queue()
				p = Process(target=f, args=('bob',q))
				p2 = Process(target=f, args=('tom',q))
				p3 = Process(target=f, args=('dick',q))
				p.start()
				p2.start()
				p3.start()
				p.join()
				p2.join()
				p3.join()

				print 'finished'
				print q.get()
				print q.get()
				print q.get()
				print ''

		if True:
				print 'start pool...'
				start_time = time.time()
				pool = Pool() 
				a=1000000
				aa=range(a,a+10)
				bb=range(10,20)
				cc = [
						'tom',
						'dick',
						'harry',
						'spleen',
						'rinkle',
						'six',
						'seven',
						'eight',
						'nine',
						'ten']
				results=pool.map(f_star, itertools.izip(aa, bb, cc))
				end_time = time.time()

				print 'took %.2f secs, results:' % (end_time-start_time)
				for (a,r) in zip(aa,results):
						print '%d: %s: %d' % (a, r[1], r[0])

				pool.close()
				print 'waiting for processes to exit...'
				pool.join()
				print 'finished.'
