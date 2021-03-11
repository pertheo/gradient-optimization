from scipy import misc
import numpy as np
import numdifftools as nd
import random
import time

def simp(x,j,max_iter,max_time):  
    y=lambda x:c+np.dot(x,b)+np.dot(x,np.dot(a,np.transpose([x])))
    iteration=0
    tr=x
    start = time.time()
    while max_iter>iteration and time.time() <= start + max_time:
        grad=nd.Gradient(y)([tr])
        t1=tr-grad*beta
        print("Iteration ",iteration+1,"\n new x:\n ",t1)
        print("J(x):\n",y(tr))
        if y(t1)<=j:
            break
        tr=t1
        iteration+=1
    return t1,y(t1)

def newton(x,j,max_iter,max_time):
    f=lambda x:c+np.dot(x,b)+np.dot(x,np.dot(a,np.transpose([x])))
    iteration=0
    start=time.time()
    while iteration<max_iter and time.time() <= start + max_time:
        grad1=nd.Gradient(f)([x])
        x1 = x - (1/misc.derivative(f, x,n=2))*grad1
        print("Iteration ",iteration+1,"\n new x:\n ",x)
        print("J(x):\n",f(x))
        if f(x1)<=j:
            break
        x=x1
        iteration=iteration+1
    return x1,f(x1)

def get_matrix(rows,columns):
    y=False
    while y==False:
        print("Enter elements of matrix: ")
        elements=list(map(int, input().split()))
        #the elements have to match given size of the matrix
        while rows*columns!=len(elements):
            print("Incorrect number of elements of matrix")
            elements=list(map(int, input().split()))
        matrix=np.array(elements).reshape(rows, columns)
        #checks if positive definite matrix
        y=check_matrix(matrix)
    return matrix

def check_matrix(a):
    at=np.transpose(a)
    for i in range(d): 
        for j in range(d): 
            if (a[i][j] != at[i][j]):
                print("Matrix is not symmetric")
                return False
    w, v = np.linalg.eig(a) 
    for x in w:
        if x<=0:
            print("Matrix is not positive definite")
            return False
    return True

def get_vector(d):
    elements=[]
    while len(elements)!=d:
        elements=list(map(int,input().split()))
    vec=np.array(elements)
    return vec

def get_random_vector(d,l,r):
    vec=[]
    for s in range(d):
        x = random.randrange(l,r+1)
        vec.append(x)
    vector=np.array(vec)
    print("Generated vector x: ",vector)
    return vector

def batch_mode(f,x,j,n):#given
    list=[]
    listy=[]
    for c in range(n):
        print(c)
        t,u=f(x,j,max_iter,max_time)
        list.append(t)
        listy.append(u)
    print("Mean of solutions (x): ",np.mean(list))
    print("Standard deviation of solutions (x): ",np.std(list))
    print("Mean of solutions J(x): ",np.mean(listy))
    print("Standard deviation of solutions J(x): ",np.std(listy))
    
def batch_mode_rand(f,j,n,l,r):#random
    list=[]
    listy=[]
    for c in range(n):
        x=get_random_vector(d,l,r)
        t,u=f(x,j,max_iter,max_time)
        list.append(t)
        listy.append(u)
    print("Mean of solutions (x): ",np.mean(list))
    print("Standard deviation of solutions (x): ",np.std(list))
    print("Mean of solutions J(x): ",np.mean(listy))
    print("Standard deviation of solutions J(x): ",np.std(listy))
    
    
    
#here main starts
k=0
d=-1
while d<=0:
    d=int(input("Enter dimension (positive scalar): "))
print("Enter 1 - to generate vector x, 2 - to enter its' elements: ")
while k!=1 and k!=2:
    k=int(input())
    if k==1:
        print("Enter start of range: ")
        l=int(input())
        r=l
        while r<=l:
            print("Enter end of range: ")
            r=int(input())
        x=get_random_vector(d,l,r)
    elif k==2:
        print("Enter elements of vector x: ")
        x=get_vector(d)
c=int(input("Enter scalar c: "))
print("Enter elements of vector b:")
bt=get_vector(d)
b=np.transpose([bt])
a=get_matrix(d,d)
j=float(input("Enter desired Jx value (float): "))
max_iter=int(input("Enter max number of iterations: "))
max_time=int(input("Enter max time (in seconds): "))

t=0
print("Enter '1' - to use simple gradient method, '2' - to use Newton's method': ")
while t!=1 and t!=2:
    t=int(input())
    if t==1:
        beta=float(input("Enter beta (float): "))
        
ch=input("Do you want to enter batch mode? (yes/no) ")
if ch=='yes' or c=='Yes':
    n=int(input("How many iterations do you want to perform? "))
    if k==1:
        if t==1:
            batch_mode_rand(simp, j, n, l, r)
        else:
            batch_mode_rand(newton, j, n, l, r)
            
    elif k==2:
        if t==1:
            batch_mode(simp, x,j,n)
        else:
            batch_mode(newton, x, j, n)
elif ch=='no' or c=='No':
    if t==1:
        sx,yx=simp(x,j,max_iter,max_time)
        print("Simple gradient method: ",sx,"\nJ(x): ",yx)
    else:
        sn,yn=newton(x,j,max_iter,max_time)
        print("Newton method: ",sn,"\nJ(x): ",yn)
