#!/usr/bin/env python
import os
import sys

in_file = open('in.txt', 'r')
out_file = open('out.txt', 'w')
p_id = 0
lines = in_file.readlines()
in_file.close()
for l in lines:
	l = l.split('\n')[0]
	l = '<p data-element-id="'+str(p_id)+'">'+l+'</p>\n'
	print l
	p_id+=1
	out_file.write(l)
out_file.close()
