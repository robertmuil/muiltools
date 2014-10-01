import numpy as np
import matplotlib.pyplot as pp


#time in 'generations'
t = np.arange(50)

#starting population at t=0
g0 = 2

#assume each generation is just a little larger than previous
growth=0.1

#calculate the number of individuals *belonging to* each generation
gens = g0*((1+growth)**t)

#assume following survival rates, over generations:
#survival=[0.0, 0.0, 0.0, 1.0] #everyone survives for exactly 1 generations
#survival=[0.0, 0.0, 1.0, 1.0] #everyone survives for exactly 2 generations
survival=[0.0, 1.0, 1.0, 1.0] #everyone survives for exactly 3 generations
#survival=[0.1, 0.5, 0.8, 1.0] #slow drop off for 4 generations

#apply the survival vector to calculate the number of individuals alive in each
# generation
population = []
dead = []
for ii in xrange(len(gens)):
	slen=len(survival)
	avail_gens=min(ii+1,slen)

	current_pop=np.dot(gens[ii+1-avail_gens:ii+1],survival[slen-avail_gens:slen])
	population.append(current_pop)
	now_dead=np.cumsum(gens[0:ii+1])[-1]-current_pop

	dead.append(now_dead)

	print '{:d}, {:d}, {:.1f}, {:.1f}'.format(ii,avail_gens, current_pop, now_dead)

pp.figure()
pp.title('g0={:d}, growth={:.1f}, survival_factor={}'.format(
	g0, growth*100.0, ','.join(['{:.1f}'.format(s) for s in survival])))

pp.plot(gens, '.-', label='individuals in each generation')
pp.plot(population,  '.-', label='population')
pp.plot(dead, '.-', label='deceased')

pp.legend()
pp.show()

pp.text(0,0,'This shows pretty clearly, that there is no way the current population could ever exceed the number of deceased even when population growth is exponential. In the real world, population growth is not near exponential, so the number of dead would be even more massively overwhelming. It is a myth and always has been.')
