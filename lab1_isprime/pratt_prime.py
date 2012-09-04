#! /usr/bin/python3
# -*- coding: utf-8 -*-
#~ 4) Pratt's Primality Test; + generation big prime

from random import randint
from math import log, exp, sqrt
import optparse

def powmod(a,k,n):
	"""(a**k) mod n"""
	b = 1
	while (k!=0):
		if (k%2==0):
			k = k//2
			a = (a*a) % n
		else:
			k -= 1
			b = (b*a) % n
	return b			 

def isprime(n,p):
	if n==2: return True
	k = len(p)
	kn = k
	for i in range(0,round(n*log(log(n)))):
		a_i = randint(2,n-1)
		check1 = powmod(a_i,n-1,n) #быстрое возведение в степень по модулю
		if (check1!=1):
			return False
		while k>0:
			#~ print(a_i)
			check2 = powmod(a_i,(n-1)//p[k-1],n)
			if (check2!=1):
				k -= 1
			else: break
		if (k==0): 
			print("a = ",a_i)
			return True
		else : kn -= 1
	
	return False

#~ -----------------
def check_Ferma(N,R):
	for i in range(N-R):
		a = randint(2,N-1)
		check1 = (powmod(a,N-1,N) == 1)
		check2 = (powmod(a,R,N) != 1) #gcd(a**R-1,N)==1)
		if check1 and check2: 
			print("Ferma check right")
			return True
		else: print("bad")
	return False
#~ ----------------------------------------------------------

def fact_2(p):
	fact = 1
	k = 0
	while fact<p-1:
		k += 1
		fact *= 2
	lf = [2 for i in range(k)]
	return lf, fact

def gen_prime(S):
	lp, res = fact_2(S)
	print ("S = ",res)
	endS = 4*S+2
	iters = 0
	while True :
		iters += 1
		beginS = res+1
		R = randint(beginS,endS)
		if (R%2==1): R+=1
		N = R*beginS+1
		if isprime(N,lp): # and check_Ferma(N,R):
			print ("\nprime : ", N, "iters = ", iters)
			break
		#~ print ("not prime", N, end = ";")
	return N

def main():	
	cl = optparse.OptionParser()
	cl.add_option("-g",action = "store_true", dest = "gen")
	cl.set_defaults(gen = False)
	opts, args = cl.parse_args()
	gen = opts.gen
	if len(args) < 2:
		print("Error!\nUsage: <program name> <input file> <output file>\n\
		OR <program name> -g <input file> <output file>\n")
		exit(1)
	f_in = open(args[0],'r')
	line = f_in.readline().split()
	n = int(line[0])
	print("n = ", n)
	f_out = open(args[1],'w')
	
	if gen:
		p = [ int(line[i]) for i in range(1,len(line))] 
		if (0<n<5): N = 5
		else: N = gen_prime(n)
		print("gen = ",N) 
		f_out.write("%d\n"%N)
	else:	
		if n==1: 
			print("0") 
			f_out.write("0\n")
			return
		if n==2 or n==3:
			print("1") 
			f_out.write("1\n")
			return
			
		p = [ int(line[i]) for i in range(1,len(line))] 
		#~ print(line,n,p)
		
		if isprime(n,p):
			print("1") 
			f_out.write("1\n")
		else:
			print("0")
			f_out.write("0\n")

if __name__ == "__main__":
	main()
