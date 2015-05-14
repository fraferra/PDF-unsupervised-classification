
class readPDF:
	
	def __init__(self, stream):
		self.stream=stream


	def processPDFContent(self):
	    import re
	    from nltk.corpus import stopwords
	    content = ""
	    # Load PDF into pyPDF
	    pdf = PyPDF2.PdfFileReader(self.stream)
	    # Iterate pages
	    for i in range(0, pdf.getNumPages()):
	        # Extract text from page and add to content
	        content += pdf.getPage(i).extractText() + "\n"
	    # Collapse whitespace
	    content = " ".join(content.replace(u"\xa0", " ").strip().split()).encode("ascii", "ignore")
	    letters_only = re.sub("[^a-zA-Z]", " ", content) 
	    #
	    # 3. Convert to lower case, split into individual words
	    words = letters_only.lower().split()                             
	    #
	    # 4. In Python, searching a set is much faster than searching
	    #   a list, so convert the stop words to a set
	    stops = set(stopwords.words("english"))                  
	    # 
	    # 5. Remove stop words
	    meaningful_words = [w for w in words if not w in stops]   
	    #
	    # 6. Join the words back into one string separated by space, 
	    # and return the result.
	    meaningful_words= ( " ".join( meaningful_words ))  
	    shortword = re.compile(r'\W*\b\w{1,4}\b')
	    longwords = re.compile(r'\W*\b\w{10,20}\b')
	    meaningful_words= shortword.sub('', meaningful_words)
	    return longwords.sub('', meaningful_words)


class Bag:

	def __init__(self, data):
		self.data=data
		

  	def bagOfWord(self):
  		words=self.data
  		from sklearn.feature_extraction.text import CountVectorizer
		# Initialize the "CountVectorizer" object, which is scikit-learn's
		# bag of words tool.  
		vectorizer = CountVectorizer(analyzer = "word",   \
		                             tokenizer = None,    \
		                             preprocessor = None, \
		                             stop_words = None,   \
		                             max_features = 5000) 

		# fit_transform() does two functions: First, it fits the model
		# and learns the vocabulary; second, it transforms our training data
		# into feature vectors. The input to fit_transform should be a list of 
		# strings.
		train_data_features = vectorizer.fit_transform(words)

		# Numpy arrays are easy to work with, so convert the result to an 
		# array
		train_data_features = train_data_features.toarray()
		return train_data_features


class Classifier:

	def __init__(self,data):
		self.data=data


	def kNN(self):

		for i in range(len(self.labels)):
			for j in range(len(self.labels)):
				tmp= scipy.spatial.distance.euclidean(self.data[i],self.data[j])

	def kMeans(self, k):
		#select random centroids
		from sklearn.cluster import KMeans
		km=KMeans(n_clusters=k)
		km.fit(self.data)
		return km.labels_


	def affinity(self):
		from sklearn.cluster import AffinityPropagation
		af = AffinityPropagation(preference=-50).fit(self.data)
		return af.labels_


	def randomCentroids(self):
		import random
		indexes= random.sample(range(len(self.data)), self.k)
		return self.data[indexes]


class DocumentsSorting:

	def __init__(self, data, label, path):
		self.data=data
		self.label=label
		self.path=path

	def sortDocuments(self):
		import os
		import os.path
		from random import randint
		uniqueData=list(set(self.data))
		libraryPath=self.path+"newLibrary"
		if os.path.exists(libraryPath):
			libraryPath=libraryPath+str(randint(1,20))
			os.system("mkdir "+libraryPath)
		else:
			os.system("mkdir "+libraryPath)
		for i in uniqueData:
			x=libraryPath+'/'+str(i)
			os.system("mkdir "+x)
		for i in range(len(self.data)):
			oldPath=self.path+self.label[i]
			newPath=libraryPath+'/'+str(self.data[i])+'/'+self.label[i]
			os.system('cp '+oldPath+' '+newPath)



if __name__=='__main__':
	import PyPDF2
	import nltk
	import scipy.spatial
	import math
	import numpy as np
	from os import listdir
	from os.path import isfile, join
	import os

	print 
	path=raw_input('Please enter path to PDF library:')

	onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) ][1:]


	list_bags=[]

	print
	print 'Reading PDFs...'
	for i in range(len(onlyfiles)):

		stream=path+onlyfiles[i]
		doc1=readPDF(stream)

		list_bags.append(doc1.processPDFContent())


	# create bag
	print 
	print 'Creating bag of words...'
	bag=Bag(list_bags)
	result=bag.bagOfWord()

	classifier=Classifier(result)


	r=classifier.kMeans(4)
	print 
	print 'Sorting clustered documents...'
	print
	doc=DocumentsSorting(r, onlyfiles, path)
	doc.sortDocuments()





	
