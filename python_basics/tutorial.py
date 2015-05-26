#implementation of a shitty sort in python

lista = [2,1,5,4,9,3]

def sort(list):
	for x in range(len(list)):
		for index, elem in enumerate(list):
			if index < (len(list) - 1):
				if elem > list[index+1]:
					list[index], list[index+1] = list[index+1], list[index]
					#list[index+1] = elem
	return list

print lista
print sort(lista)

# class Person:
#     population = 0
#     def __init__(self, myAge):
#         self.age = myAge
#         Person.population += 1
#     def self.get_population(self):
#         return Person.population
#     def get_age(self):
#         return self.age

# p1 = Person(63)
# p2 = Person(15)
# print p1.get_population()
# print Person.get_population()



# #implementation of quicksort in python

# def quicksort(list):
# 	pivot = list[0]
# 	leftList = []
# 	rightList = []
# 	for elem in list:
# 		if elem < pivot:
# 			leftList.append(elem)
# 		else:
# 			rightList.append(elem)
# 		if len(leftList) >= (len(list)-2):
# 			return leftList
# 		else: 
# 			quicksort(leftList + rightList)	

# print quicksort(lista)