import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split 
from DiseaseIndicator.DiseaseIndicator.stack import Stack
from DiseaseIndicator.DiseaseIndicator.KNN import KNN


sympDictionary=pd.read_csv('symptomps.csv').to_dict()
name= input("Enter the Symptoms: ")
symptom = sympDictionary[name]
symptomList=list(symptom.values())

filterSymptomps = [s for s in symptomList if str(s) != 'nan']

visited=[]

def allMatched(l1, l2):
    
    for j in l1:
        if j in l2:
            continue
        else:
            return 0
    return 1
    


for i in filterSymptomps:
    if i not in visited:
        visited.append(i)
        if i != name:
            
            print(i)
            b=sympDictionary[i]
            b=list(b.values())

            n = [i for i in b if str(i) != 'nan']
            
            if(allMatched(n,visited)==0):
                for j in n:
                    if j not in visited:
                        visited.append(j)                       
                        


def dfs(symDictioary):
    
    FStack = Stack()   
    FStack.push((symDictioary, [])) # [] will be use for path

    while not FStack.isEmpty():
        state,exp = FStack.pop()
        
        if(allMatched(state,exp)==1):
            return exp
        
        for neighbor in state:
            if neighbor not in exp:
                exp.append(neighbor)
                FStack.push((neighbor, exp))


print("")
res=dfs(filterSymptomps)
print(res)
print("okay")



    
inputList= [0 for x in range(0,132)]
    
symp=list(sympDictionary.keys())

for element in res:
    for k in range(0,131):
        if(element==symp[k]):
            inputList[k]=1

print(inputList)                

inputList=np.array([inputList])




data = pd.read_csv("C:\\Users\\malis\\Desktop\\sem5\\AI_Lab\\__Project\\dataSet.csv")  

X = data.to_numpy()   
X = X[:,0:132]

Y = data.to_numpy()  
Y = Y[:,132]


X_Features_Train, X_Features_Test, y_Feature_Train, y_Feature_Test = train_test_split(X,Y,test_size=0.2, random_state=111) 



clf=KNN(5)
clf.fit(X_Features_Test, X_Features_Train, y_Feature_Test, y_Feature_Train)

# pre=clf.predict(X_Features_Test)
# print(clf.accuracy)
# print(clf.prediction[0][0])
print()

#X_test = np.array([[0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]])
pre=clf.predict(inputList)
print(clf.prediction[0][0])
A=clf.get_accuracy(inputList)
print(A)

