from django.http import  HttpResponse
from django.shortcuts import render
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from . import stack as S
from . import KNN as K
import  chime
chime.theme("big-sur")


def start(request):
    import pyaudio
    import speech_recognition as sr
    r = sr.Recognizer()

    import pyttsx3

    eng = pyttsx3.init()
    eng.setProperty('rate', 135)
    voices = eng.getProperty('voices')
    eng.setProperty('voice', voices[0].id)

    def sayToSpeaker(text):
        eng.say(text)
        eng.runAndWait()

    sayToSpeaker("Welcome. Say yes, if you want to start the audio system. Otherwise say no.")

    with sr.Microphone() as source:
        chime.success()
        audio = r.listen(source)

    try:
        chime.info()
        if "yes" in r.recognize_google(audio).__str__().lower():
            sayToSpeaker("We are initiating the Audio System. Let's get started")
            print("")
            return render(request,'a_home.html')

        if "no" in r.recognize_google(audio).__str__().lower():
            sayToSpeaker("We are getting to the Visual Page")
            return render(request, 'symtomps.html')

    except LookupError:
        print("Could not understand audio")
    except Exception as e:
        print("Could not understand audio")
    return render(request, 'symtomps.html')

def index(request):
    return render(request,'index.html')

def getSymptopm(request):
    return render(request,'symtomps.html')


ResSymp=[]
def detSymptopm(request):
    sympDictionary = pd.read_csv(r"D:\PythonProjects\TermProject\DiseaseIndicator\static\DiseaseIndicator\symptomps.csv").to_dict()
    name = request.POST.get('input', 'chills')

    symptom = sympDictionary[name]
    symptomList = list(symptom.values())

    filterSymptomps = [s for s in symptomList if str(s) != 'nan']

    def allMatched(l1, l2):

        for j in l1:
            if j in l2:
                continue
            else:
                return 0
        return 1

    def dfs(symDictioary):

        FStack = S.Stack()
        FStack.push((symDictioary, []))  # [] will be use for path

        while not FStack.isEmpty():
            symp, exp = FStack.pop()

            if (allMatched(symp, exp) == 1):
                return exp

            for neighbor in symp:
                if neighbor not in exp:
                    exp.append(neighbor)

                    temp = sympDictionary[neighbor]
                    temp = list(temp.values())

                    n = [i for i in temp if str(i) != 'nan']

                    for x in n:
                        if (x not in symp) and (x != neighbor):
                            symp.append(x)
                    symp.remove(neighbor)
                    FStack.push((symp, exp))

    res = dfs(filterSymptomps)
    global ResSymp
    ResSymp = []
    ResSymp=res

    resultDictionary = { "list1": res , 'sym':name}

    return render(request,'detailsSymtomps.html', resultDictionary)

def calculate(request):
    global ResSymp
    temp=ResSymp
    inputList = [0 for x in range(0, 132)]
    sympDictionary = pd.read_csv( r"D:\PythonProjects\TermProject\DiseaseIndicator\static\DiseaseIndicator\symptomps.csv").to_dict()
    symp = list(sympDictionary.keys())


    for element in temp:
        if request.POST.get(element, 'off')=="on":
            for k in range(0, 131):
                if (element == symp[k]):
                    inputList[k] = 1

    data = pd.read_csv(r"D:\PythonProjects\TermProject\DiseaseIndicator\static\DiseaseIndicator\dataSet.csv")

    X = data.to_numpy()
    X = X[:, 0:132]

    Y = data.to_numpy()
    Y = Y[:, 132]

    X_Features_Train, X_Features_Test, y_Feature_Train, y_Feature_Test = train_test_split(X, Y, test_size=0.2,
                                                                                          random_state=111)

    clf = K.KNN(5)
    clf.fit(X_Features_Test, X_Features_Train, y_Feature_Test, y_Feature_Train)
    inputList = np.array([inputList])

    # X_test = np.array([[0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]])
    clf.predict(inputList)
    disease=clf.prediction[0][0]
    Accuracy = clf.get_accuracy(inputList)

    import csv
    precautionDictionary = {}
    with open(r"D:\PythonProjects\TermProject\DiseaseIndicator\static\DiseaseIndicator\symptomPrecaution.csv") as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            prec = {row[0]: [row[1], row[2], row[3], row[4]]}
            precautionDictionary.update(prec)

    description_list={}
    with open(r"D:\PythonProjects\TermProject\DiseaseIndicator\static\DiseaseIndicator\symptomDescription.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            description = {row[0]: row[1]}
            description_list.update(description)


    resultInfo= {
        'DiseaseName': disease,
        'Accuracy': Accuracy,
        'DiseaseDescription': description_list[disease],
        'Precautions': precautionDictionary[disease]
    }

    return render(request,'result.html', resultInfo)

def audioGetSymptom(request):
    return render(request,'a_home.html')

AudioResSymp=[]
def audioDetSymptopm(request):

    sympDictionary = pd.read_csv(r"D:\PythonProjects\TermProject\DiseaseIndicator\static\DiseaseIndicator\audioSymptomp.csv").to_dict()
    name = request.POST.get('input', 'chills')

    symptom = sympDictionary[name]
    symptomList = list(symptom.values())

    filterSymptomps = [s for s in symptomList if str(s) != 'nan']

    def allMatched(l1, l2):

        for j in l1:
            if j in l2:
                continue
            else:
                return 0
        return 1

    def dfs(symDictioary):

        FStack = S.Stack()
        FStack.push((symDictioary, []))  # [] will be use for path

        while not FStack.isEmpty():
            symp, exp = FStack.pop()

            if (allMatched(symp, exp) == 1):
                return exp

            for neighbor in symp:
                if neighbor not in exp:
                    exp.append(neighbor)

                    temp = sympDictionary[neighbor]
                    temp = list(temp.values())

                    n = [i for i in temp if str(i) != 'nan']

                    for x in n:
                        if (x not in symp) and (x != neighbor):
                            symp.append(x)
                    symp.remove(neighbor)
                    FStack.push((symp, exp))

    res = dfs(filterSymptomps)
    global AudioResSymp
    AudioResSymp=[]
    AudioResSymp=res

    resultDictionary = { "list1": res , 'sym':name}

    return render(request,'audioDetailsSymtomps.html', resultDictionary)

audioResultInfo={}
def audioCalculate(request):

    inputList = [0 for x in range(0, 132)]
    sympDictionary = pd.read_csv(
        r"D:\PythonProjects\TermProject\DiseaseIndicator\static\DiseaseIndicator\symptomps.csv").to_dict()
    symp = list(sympDictionary.keys())


    import pyaudio
    import speech_recognition as sr
    r = sr.Recognizer()


    import pyttsx3

    eng = pyttsx3.init()
    eng.setProperty('rate', 135)
    voices = eng.getProperty('voices')
    eng.setProperty('voice', voices[1].id)

    def sayToSpeaker(text):
        eng.say(text)
        eng.runAndWait()

    sayToSpeaker("Answer me some questions in Yes or No. Say STOP to end this questionnaire")

    global AudioResSymp

    for element in AudioResSymp:
        sayToSpeaker("Are you Suffering from " + element + ".")
        with sr.Microphone() as source:
            chime.success()
            audio = r.listen(source)

        try:
            chime.info()
            if "yes" in r.recognize_google(audio).__str__().lower():
                print(r.recognize_google(audio).__str__().lower())
                print(element)
                for k in range(0, 131):
                    if (element == symp[k]):                        
                        inputList[k] = 1

            if "stop" in r.recognize_google(audio).__str__().lower():
                break

        except LookupError:
            print("Could not understand audio")


    data = pd.read_csv(r"D:\PythonProjects\TermProject\DiseaseIndicator\static\DiseaseIndicator\dataSet.csv")

    X = data.to_numpy()
    X = X[:, 0:132]

    Y = data.to_numpy()
    Y = Y[:, 132]

    X_Features_Train, X_Features_Test, y_Feature_Train, y_Feature_Test = train_test_split(X, Y, test_size=0.2,
                                                                                          random_state=111)

    clf = K.KNN(5)
    clf.fit(X_Features_Test, X_Features_Train, y_Feature_Test, y_Feature_Train)
    inputList = np.array([inputList])

    # X_test = np.array([[0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0]])
    clf.predict(inputList)
    disease=clf.prediction[0][0]
    Accuracy = clf.get_accuracy(inputList)

    import csv
    precautionDictionary = {}
    with open(r"D:\PythonProjects\TermProject\DiseaseIndicator\static\DiseaseIndicator\symptomPrecaution.csv") as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            prec = {row[0]: [row[1], row[2], row[3], row[4]]}
            precautionDictionary.update(prec)

    description_list={}
    with open(r"D:\PythonProjects\TermProject\DiseaseIndicator\static\DiseaseIndicator\symptomDescription.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            description = {row[0]: row[1]}
            description_list.update(description)

    global audioResultInfo
    audioResultInfo= {
        'DiseaseName': disease,
        'Accuracy': Accuracy,
        'DiseaseDescription': description_list[disease],
        'Precautions': precautionDictionary[disease]
    }

    return render(request,'audioResults.html', audioResultInfo)

#this function use for audiolize the results
def audioCalculateResult(request):
    import pyaudio
    import speech_recognition as sr
    r = sr.Recognizer()
    import pyttsx3

    eng = pyttsx3.init()
    eng.setProperty('rate', 135)
    voices = eng.getProperty('voices')
    eng.setProperty('voice', voices[1].id)

    def sayToSpeaker(text):
        eng.say(text)
        eng.runAndWait()   


    global audioResultInfo

    sayToSpeaker("Our System had predicted that you MIGHT have " + str(round(audioResultInfo["Accuracy"],2)) + "%  chance of " + audioResultInfo["DiseaseName"])
    sayToSpeaker("These results are generated by computer. Consult the Doctor for final words.")
    sayToSpeaker("Say Yes if you want to listen Description and precautionary measurements?")

    with sr.Microphone() as source:
        chime.success()
        audio = r.listen(source)

    try:
        chime.info()
        if "yes" in r.recognize_google(audio).__str__().lower():
            print(r.recognize_google(audio).__str__().lower())
            sayToSpeaker(audioResultInfo["DiseaseDescription"])
            sayToSpeaker("Here are the Precautions ")
            for pre in audioResultInfo["Precautions"]:
                if pre != "":
                    sayToSpeaker(pre)

    except LookupError:
        print("Could not understand audio")
    return render(request,'result.html', audioResultInfo)

