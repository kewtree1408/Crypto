#! /usr/bin/python3
# -*- coding: utf-8 -*-

# a^x = b(mod p)

import sys
from random import randint

def eGCD(a, b):
	if b == 0:
		return a , 1, 0
	d1, x1, y1 = eGCD(b, a%b )
	d, x, y = d1, y1, x1 - (a//b)*y1
	return d, x, y

def get_inv(x,y):
	d, ax, ay = eGCD(x,y)
	if d<=1: return ax
	print("Error")
	exit(-1) 

def get_alpha(q):
	q.sort();
	q_p = {}
	k = 1
	q_p[q[0]] = k
	for i in range(1,len(q)):
		if q[i]==q[i-1]: k += 1
		else: k = 1	
		q_p[q[i]] = k
	return q_p

def get_table(a,p,q):
	t = {}
	for qi in q:
		t[qi] = [ pow(a,j*(p-1)//qi,p) for j in range(0,qi) ]
	#~ print("table = ",t)
	return t

def get_china_coeff(a,b,p,r,q,q_al):
	x_f = {} #finished map
	for qi in q:
		x = []
		c = pow(b,(p-1)//qi,p)
		x.append(r[qi].index(c))
		pow_sum = 0
		for i in range(1,q_al[qi]): # проходим по все alpha_i у данного qi
			pow_sum += x[i-1]*(qi**(i-1))
			c = pow(b*get_inv((a**pow_sum),p),(p-1)//(qi**(i+1)), p)
			x.append(r[qi].index(c))
		x_f[qi**q_al[qi]] = sum([xi*qi**i for i,xi in enumerate(x) ])
				
	return x_f
	
def china(coeff, p):
	m = list(coeff)
	M = [ (p-1)//mi for mi in m]
	a = [ coeff[mi] for mi in m]
	b = [ get_inv(Mi,mi) for Mi,mi in zip(M,m) ]
	x = sum([ Mi*ai*bi for Mi,ai,bi in zip(M,a,b) ])%(p-1)
	return x
	

def dlog(a,b,p,q):
	#~ map: key == qi, value == alpha_i
	q_al = get_alpha(q)
	#~ print(q_al)
	
	#~ map: key == qi, value == powmod(a,j*(p-1)//qi,p)
	r = get_table(a,p,q)
	#~ print(r)
	
	#~ map: key = x[i], value == list foreach qi(alpha_i)
	coeff = get_china_coeff(a,b,p,r,q,q_al)
	#~ print(coeff)
	
	x = china(coeff,p)
	return x
	
def main():
	if len(sys.argv)<3:
		print("Error!\nUsage: <program name> <input file> <output file>\n")
		exit(1)
	
	f_in = open(sys.argv[1],'r')
	line = f_in.readline().split()
	a, b, p = [ int(n) for n in line[:3] ]
	q = [ int(n) for n in line[3:]]
	
	f_out = open(sys.argv[2],'w')
	x = dlog(a,b,p,q)
	f_out.write("%d\n"%x)
	
	#~ debug
	if pow(a,x,p)==b:
		print("TRUE!111")
	else: print("FAIL =(")
	print(x)
	
if __name__ == "__main__":
	main()	
