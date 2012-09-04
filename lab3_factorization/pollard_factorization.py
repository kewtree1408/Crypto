#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from random import randint, randrange
#~ from math import abs

def miller_rabin(n, r=100):
	if n==2: return True
	
	t = n-1
	s = 0
	while t % 2 == 0:
		t //= 2
		s += 1
		
	for i in range(r):
		a = randint(2,n-1)
		x = pow(a,t,n)
		if x==1 or x==n-1: continue
		for k in range(1,s):
			x = pow(x,2,n)
			if x==1: return False
			if x==n-1: break
		if x==n-1: continue
		return False
	return True

def f(x,n): return ( x*x+randint(2,n) )%n
def gcd(a,b): return a if b==0 else gcd(b,a%b)
def isprime(p): return miller_rabin(p)

def pollard(n, k = 2**15):
	"""Pollard factorization"""
	x = y = randint(2,n) #not circle 
	#~ print (x,y)
	#~ x_2i == y_i
	for i in range(k):
		x = f(x,n)
		y = f(y,n)
		y = f(y,n)
		d = gcd(abs(x-y),n)
		#~ print (d)
		if 1 < d < n:
			return d
		elif d == n: 
			return None
	return None

def fact(n):
	if isprime(n): return n
	if n%2==0: return 2
	return pollard(n)

def main():
	if len(sys.argv)<3:
		print("Error!\nUsage: <program name> <input file> <output file>\n")
		exit(1)
	
	f_in = open(sys.argv[1],'r')
	n = int(f_in.read())
	print(sys.argv[1])
	
	#~ n = randrange(1,10000,2)
	#~ print ("n = ",n)
	
	if n<=1:
		print("Fail input %d\n"%n)
		return -1

	p = fact(n)
	if (p==None):
		print("Fail factorization %d\n"%n)
		return -1
	q = n//p
	
	f_out = open(sys.argv[2],'w')
	f_out.write("%d %d\n"%(p,q))
	
	print("n = ",n,"p = ",p,"q = ",q)


def test():
	while True:
		n = randrange(1,2**256+10,2)
		if n<=1:
			print("Fail input %d\n"%n)
			return -1

		p = fact(n)
		if (p==None):
			print("Fail factorization %d\n"%n)
			return -1
		q = n//p
		
		print ("n = ",n,"p = ",p,"q = ",q)
		

	
if __name__ == "__main__":
	 main()
	 #~ test()
