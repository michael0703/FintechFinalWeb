from django.shortcuts import render,redirect   # 加入 redirect 套件
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
import datetime
from .models import ClientRecord
import collections
import jieba

# Create your views here.

def getCallOutNum(clientRecord):

	HistoryID = [record.clientID for record in clientRecord]
	obj = dict(collections.Counter(HistoryID))
	d = {}
	for key in obj:
		if obj[key] not in d:
			d[obj[key]] = 0
		d[obj[key]] += 1
	return d


def getProductRank(clientRecord):

	d = {}
	for record in clientRecord:
		Uniformfield = record.Uniformfield.split(":")[1]
		product = Uniformfield.split(";")
		for tmp in product:
			if tmp == "":
				continue
			if tmp not in d:
				d[tmp] = 0
			d[tmp] += 1
	return d

def getMixedText(clientRecord):

	mixedText = ""
	for record in clientRecord:

		oneline = jieba.cut(record.Nonuniformfield)
		oneline = " ".join(oneline)
		mixedText += (" " + oneline)

	return mixedText

def MainPage(request):

	interestedProduct = ["產品1", "產品2", "產品3", "產品4", "產品5"]
	

	return render(request, "MainPage.html", locals())
	# return HttpResponse("Hello, World!")

def Process(request):

	interestedProduct = ["產品1", "產品2", "產品3", "產品4", "產品5"]

	if request.method == "POST":
		# print(request.POST)
		interestedCount = int(request.POST['countvar'])
		clientID = request.POST.get('clientid')
		callOutDate = request.POST.get('calloutdate')
		NonUniformArea = request.POST.get('NonUniformArea')
		UniformArea = []

		for i in range(1, interestedCount+1):

			try:
				index = int(request.POST.get(str(i)))
				UniformArea.append(interestedProduct[index-1])
			except:
				continue
			
		print(clientID, callOutDate, NonUniformArea, UniformArea)
		newRecord = ClientRecord()
		try:
			newRecord.clientID = clientID
			newRecord.calloutDate = datetime.datetime.strptime(callOutDate, "%Y-%m-%d")
			newRecord.Uniformfield = "有興趣:" + ";".join(UniformArea)
			newRecord.Nonuniformfield = NonUniformArea

			newRecord.save()
		except:
			errmsg = "你有東西沒填對！"
			return render(request, "MainPage.html", locals())

		# print(newRecord.clientID, newRecord.callOutDate, newRecord.Uniformfield, newRecord.Nonuniformfield)
		

	return redirect("/")

def QueryNonuniform(request):


	if request.method == 'GET':
		return render(request, "QueryNonuniform.html")
	else:
		if request.POST['filterword'] == "":
			return render(request, "QueryNonuniform.html")	
		clientRecord1 = ClientRecord.objects.filter(Nonuniformfield__contains=request.POST['filterword'])
		clientRecord2 = ClientRecord.objects.filter(Uniformfield__contains=request.POST['filterword'])
		clientRecord = clientRecord1 | clientRecord2
		return render(request, "QueryNonuniform.html", locals())


def ListDB(request):

	clientRecord = ClientRecord.objects.all()

	return render(request, "ListDB.html", locals())

def Analyze(request):

	clientRecord = ClientRecord.objects.all()
	CallOutNumDict = getCallOutNum(clientRecord)
	print("CallOutNumDict: ", CallOutNumDict)

	InterestProductRank = getProductRank(clientRecord)
	print("InterestProductRank: ", InterestProductRank)

	# getWordCloudText = getMixedText(clientRecord)
	# print("getWordCloudText: ", getWordCloudText)

	return render(request, "Analyze.html", locals())

def Query(request):

	if request.method == 'GET':
		return render(request, "Query.html")
	else:

		clientRecord = ClientRecord.objects.filter(clientID=request.POST['clientID'])
		return render(request, "Query.html", locals())



