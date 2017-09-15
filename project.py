from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import math
def str2int(s):
	numbers={'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'zero':0}
	if(s.isdigit()):
		return int(s)
	elif(s==''):
		return -1
	else:
		return numbers[s]
class coins(object):
	def __init__(self,postags,words):
		self.numbers=[]
		self.get_numbers(postags)
		self.keyword=' '
		self.keywords=1
		self.head=' '
		self.tail=' '
		self.coinindex=0
		self.headindex=0
		self.tailindex=0
		self.keywordindex=0
		self.h=0
		self.t=0
		if('head' in words and 'tail' in words):
			self.head='head'
			self.tail='tail'
			self.headindex=words.index('head')
			self.tailindex=words.index('tail')
			self.coinindex=words.index('coin')
			self.keywords=2
		else:
			if('head' in words):
				self.keyword='head'
				self.keywordindex=words.index('head')
				self.coinindex=words.index('coin')
				self.keywords=1
			elif('tail' in words):
				self.keyword='tail'
				self.keywordindex=words.index('tail')
				self.coinindex=words.index('coin')
				self.keywords=1
		self.post=True
		if(self.keywords==2):
			if(self.coinindex>(max(self.headindex,self.tailindex))):
				print '1'
				self.post=True
				if(self.headindex>self.tailindex):
					self.h=self.numbers[1]
					self.t=self.numbers[0]
				else:
					self.h=self.numbers[0]
					self.t=self.numbers[1]
			else:
				print '2'
				self.post=False
				if(self.headindex>self.tailindex):
					self.h=self.numbers[2]
					self.t=self.numbers[1]
				else:
					self.h=self.numbers[1]
					self.t=self.numbers[2]
		elif(self.keywords==1):
			if(self.coinindex>self.keywordindex):
				self.post=True
			else:
				self.post=False

	def get_numbers(self,postags):
		self.cds=['','','']
		self.index=-1;
		self.previndex=-1;
		for word in range(len(postags)):
			if(postags[word][1]=='CD'):
				if(word==(self.previndex+1)):
					if(self.index==-1):
						self.index=0
					self.cds[self.index] +=postags[word][0]
				else:
					self.index+=1
					self.cds[self.index] =self.cds[self.index]+postags[word][0]
				self.previndex=self.previndex+1
		for s in self.cds:
			self.numbers.append(str2int(s))	
	def print_variables(self):
		print self.numbers
		print self.keyword
		print self.coinindex
		print self.keywordindex
		print self.post
		print self.head
		print self.headindex
		print self.tail
		print self.tailindex
		print self.keywords
		print self.h
		print self.t
	def find_probability(self):
		self.cases=[]
		self.appcases=0
		if(self.keywords==1):
			if(not self.post):
				for i in range(int(math.pow(2,self.numbers[0]))):
					self.case=[]
					self.bits='{0:09b}'.format(i)
					for c in self.bits[9-self.numbers[0]:]:
						if(c=='1'):
							self.case.append(1)
						else:
							self.case.append(0)
					self.cases.append(self.case)		
			else:
				for i in range(int(math.pow(2,self.numbers[1]))):
					self.case=[]
					self.bits='{0:09b}'.format(i)
					for c in self.bits[9-self.numbers[1]:]:
						if(c=='1'):
							self.case.append(1)
						else:
							self.case.append(0)
					self.cases.append(self.case)
			self.appcases=0.0
			if(not self.post):
				if(self.numbers[1]>self.numbers[0]):
					return  "Invalid Question\n"
				else:
					for case in self.cases:
						if(self.keyword=='head'):
							if(sum(case)==self.numbers[1]):
								self.appcases+=1
						if(self.keyword=='tail'):
							if((self.numbers[0]-sum(case))==self.numbers[1]):
								self.appcases+=1
					return self.appcases/len(self.cases)			
			else:
				if(self.numbers[0]>self.numbers[1]):
					return  "Invalid Question\n"
				else:
					for case in self.cases:
						if(self.keyword=='head'):
							if(sum(case)==self.numbers[0]):
								self.appcases+=1
						if(self.keyword=='tail'):
							if((self.numbers[1]-sum(case))==self.numbers[0]):
								self.appcases+=1
					return self.appcases/len(self.cases)
		else:
			if(not self.post):
				for i in range(int(math.pow(2,self.numbers[0]))):
					self.case=[]
					self.bits='{0:09b}'.format(i)
					for c in self.bits[9-self.numbers[0]:]:
						if(c=='1'):
							self.case.append(1)
						else:
							self.case.append(0)
					self.cases.append(self.case)		
			else:
				for i in range(int(math.pow(2,self.numbers[2]))):
					self.case=[]
					self.bits='{0:09b}'.format(i)
					for c in self.bits[9-self.numbers[2]:]:
						if(c=='1'):
							self.case.append(1)
						else:
							self.case.append(0)
					self.cases.append(self.case)
			self.appcases=0.0
			if(self.post):
				if((self.h+self.t)>self.numbers[2]):
					return  "Invalid Question\n"
				else:
					for case in self.cases:
						if(sum(case)>=self.h and (self.numbers[2]-sum(case))>=self.t):
							self.appcases+=1
					return self.appcases/len(self.cases)			
			else:
				if((self.h+self.t)>self.numbers[0]):
					return  "Invalid Question\n"
				else:
					for case in self.cases:
						if(sum(case)>=self.h and (self.numbers[0]-sum(case))>=self.t):
							self.appcases+=1
					return self.appcases/len(self.cases)

def main():
	ps=PorterStemmer()
	wl=WordNetLemmatizer()
	print "1-->To test probability\n"
	print "0-->To Exit\n"
	choice=input("Enter your choice\n")
	while(choice!=0):
		question=raw_input("Enter the question..\n").lower()
		sent_words=word_tokenize(question)
		pos_tags=nltk.pos_tag(sent_words)	
		for i  in range(len(sent_words)):
			sent_words[i]=wl.lemmatize(sent_words[i])						
		coin=coins(pos_tags,sent_words)
		print question
		print sent_words
		print pos_tags
		#coin.print_variables()	
		print "Probability=" ,coin.find_probability()
		print "1-->To test probability\n"
		print "0-->To Exit\n"
		choice=input("Enter your choice\n")		
if __name__=="__main__":
	main()				



