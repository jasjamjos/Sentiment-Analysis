# from collections import OrderedDict

# class decisiontable:

# 	def buildClassifier(data):
		
# 		numInstances = len(data)
# 		list(dict.fromkeys(data))

from collections import Counter


words = ['a', 'b', 'c', 'a']

Counter(words).keys() # equals to list(set(words))
Counter(words).values() # counts the elements' frequency
print(Counter(words).values())


		