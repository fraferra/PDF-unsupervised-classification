
#CONSTANTS
PATH='/Users/fraferra/Documents/Revision/Numerical Methods/Past papers/'

PAPERS=[2008,2009,2010,2011,2012,2013,2014]

EXT='.pdf'

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
	    return( " ".join( meaningful_words ))  


  	def bagOfWord(self):
  		words=[self.processPDFContent()]
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

	#def randomForestClassifier(self):


if __name__=='__main__':
	import PyPDF2
	import nltk
	list_bags=[]
	#nltk.download() 
	#import readPDF
	for i in range(7):
		print i
		stream=PATH+str(PAPERS[i])+EXT
		doc1=readPDF(stream)
		list_bags.append(doc1.bagOfWord()[0])
	#bag1=createBagsOfWords()

	print list_bags
	#print bag1.bagOfWord([doc1])



	#print PyPDF2.PdfFileReader(STR).getNumPages()
