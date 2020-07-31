from PIL import Image
import numpy as np
print("Please wait....")
img=Image.open('tiny.png')
img=img.convert('RGB')
arr=np.array(img)
#0 is black and 255 is white
h=img.size[0]
w=img.size[1]
for i in range(w):
    if(arr[0][i][0]==255):
        frst=i
    if(arr[h-1][i][0]==255):
        last=i
# Now we will convert maze into a graph so we will mark some nodes.
node_l=[]
node_l.append(frst)
for i in range(1,h-1):
    for j in range(1,w-1):
        (c1,c2)=(0,0)
        if(arr[i][j-1][0]== 255 and arr[i][j+1][0]==255 and arr[i-1][j][0]==0 and arr[i+1][j][0]==0 and arr[i][j][0]==255):
            c1=1
        if(arr[i][j-1][0]== 0 and arr[i][j+1][0]==0 and arr[i-1][j][0]==255 and arr[i+1][j][0]==255 and arr[i][j][0]==255):
            c2=1
        elif(arr[i][j][0] != 0 and c1==0):
            node_l.append(i*h+j+1)
node_l.append((h-1)*w+last+1)
#Now after marking the nodes lets connect them if possible by an edge
# All the elements of v1 and v2 which have the same index are connected by an edge
v1=[]                                       
v1.append(node_l[0]+1)              #Adding the START point
v2=[]
v2.append(node_l[0]+h+1)        #Adding point which is just below the start as we will enter from there
for p in range(1,len(node_l)):
    stop=(node_l[p])%h
    c=stop-1
    stop=stop-2
    lvl=(node_l[p])//h
    j=lvl
    while(arr[lvl][stop][0]!=0):
        chk=lvl*h+stop+1
        if chk in node_l:
            v1.append(node_l[p])
            v2.append(chk)
            break
        stop=stop-1
    j=j-1
    while(arr[j][c][0]!=0):
        chk=j*h+c+1
        if chk in node_l:
            v1.append(node_l[p])
            v2.append(chk)
            break
        j=j-1
trial=list(set(v1+v2))
trial.sort()
# final is an adjacency matrix
final = [[0 for col in range(len(trial))] for row in range(len(trial))]
for i in range(len(v1)):
    chn1=trial.index(v1[i])
    v1[i]=chn1
    chn2=trial.index(v2[i])
    v2[i]=chn2
    final[chn1][chn2]=1
    final[chn2][chn1]=1
def precedence(graph,s):  #To find the precedence of each vertex which is closest to the source
    p=[]
    c=[]
    for i in range(len(graph[0])):
        p.append(0)
        c.append(-1)
    p[s]=0    
    q=[]
    c[s]=1
    q.append(s)
    while len(q)!=0:
        t=q[0]
        q.remove(q[0])
        for i in range(len(graph[0])):
            if graph[t][i]==1 and c[i]!=1:
                q.append(i)
                p[i]=t
                c[i]=1
    return p
def path(p,e,s):# To return the path
    b=[]
    b.append(e)
    while p[e]!=0:
        e=p[e]
        b.append(e)
    b.append(s)
    b.reverse()
    return b
p=precedence(final,0)
# vox is having the final path stored as a list.
vox=path(p,len(final)-1,0)
for i in range(len(vox)-1):
    star= trial[vox[i]]
    end=trial[vox[i+1]]
    star1=star//h
    star2=star%h
    star2=star2-1
    end1=end//h
    end2=end%h
    end2=end2-1
    if(star1==end1):
        if(star2<end2):
            for j in range(star2,end2+1):
                arr[star1][j]=[220,45,45]
        else:
            for j in range(end2,star2+1):
                arr[star1][j]=[220,45,45]
    if(star2==end2):
        if(star1<end1):
            for j in range(star1,end1+1):
                arr[j][star2]=[220,45,45]
        else:
            for j in range(end1,star1):
                arr[j][star2]=[220,45,45]
print("The path of color Brown has been drawn over the image by using Breadth First Search algorithm")
#The way to save image
im = Image.fromarray(arr)
im.save("your_file.png")    
