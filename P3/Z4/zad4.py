#!/usr/bin/python3

def B(i,j):
    return 'B_%d_%d' % (i,j)
    
def storms(rows, cols, triples):
    writeln(':- use_module(library(clpfd)).')

    cols = list(cols)
    rows = list(rows)
        
    R = len(rows)
    C = len(cols)
    
    bs = [ B(i,j) for i in range(R) for j in range(C)]
    
    writeln('solve([' + ', '.join(bs) + ']) :- ')
    
    writeln('[' + ', '.join(bs) + '] ins 0..1,')
    
    iter = 0   
    for row in rows:
        rowSum = [B(iter,j) for j in range(C)]
        writeln('sum(['+', '.join(rowSum) + '], #=, ' + str(row) + '), ')
        iter+=1

    iter = 0
    for col in cols:
        colSum = [B(i, iter) for i in range(R)]
        writeln('sum(['+', '.join(colSum) + '], #=, ' + str(col) + '), ')
        iter+=1
        
    goodTriples = "[[0, 0, 0], [1, 0, 0], [0, 0, 1], [1, 1, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]]"
    goodSquares = "[[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1], [0, 1, 0, 0], [0, 1, 0, 1], [1, 0, 0, 0], [1, 0, 1, 0], [1, 1, 0, 0], [1, 1, 1, 1]]"

    for j in range(C):
        for i in range(R-2):
            writeln('tuples_in( [['+B(i,j)+', '+B(i+1,j)+', '+B(i+2,j)+']], '+goodTriples+'),')
    
    for j in range(C-2):
        for i in range(R):
            writeln('tuples_in( [['+B(i,j)+', '+B(i,j+1)+', '+B(i,j+2)+']], '+goodTriples+'),')

    for j in range(C-1):
        for i in range(R-1):
            writeln('tuples_in( [['+B(i,j)+', '+B(i+1,j)+', '+B(i,j+1)+', '+B(i+1,j+1)+']], '+goodSquares+'), ')
    
    for x, y, val in triples:
        writeln(B(x,y)+' #= '+str(val)+', ')

    writeln('    labeling([ff], [' +  ', '.join(bs) + ']).' )
    writeln('')
    writeln(":- tell('prolog_result.txt'), solve(X), write(X), nl, told.")

def writeln(s):
    output.write(s + '\n')

txt = open('zad_input.txt').readlines()
output = open('zad_output.txt', 'w')

rows = map(int, txt[0].split())
cols = map(int, txt[1].split())
triples = []

for i in range(2, len(txt)):
    if txt[i].strip():
        triples.append(map(int, txt[i].split()))

storms(rows, cols, triples)            
