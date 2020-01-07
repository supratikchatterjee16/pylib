import os
import sys
import math

__all__ = ['mimetypes','signatures','download_signatures']

import afi.mimetypes as mimetypes
import afi.signatures as signatures
import afi.download_signatures as update

extensions_list = mimetypes.list
signatures_list = signatures.list

def search_signatures(file_bytes, lower_index = 0, upper_index = len(signatures_list)-1):
	index = math.floor((lower_index + upper_index) / 2)
	compare_element = signatures_list[index][1]
	compare_bytes = file_bytes[:len(compare_element)]
	if compare_element == compare_bytes:
		#when found perform a localized search for all possibilities
		start = index
		end = index
		x = ''
		while True:
			x = signatures_list[start][1]
			if len(x) >= len(compare_bytes) and x[:len(compare_bytes)] == compare_bytes:
				start-=1
			else:
				break
		while True:
			x = signatures_list[end][1]
			if len(x) >= len(compare_bytes) and x[:len(compare_bytes)] == compare_bytes:
				end+=1
			else:
				break
		if start!= end:
			return [extension[0] for extension in signatures_list[start:end]]
		else:
			return [signatures_list[start][0]]
	if  compare_element < compare_bytes:
		lower_index = index + 1
	elif  compare_element > compare_bytes:
		upper_index = index - 1
	if lower_index != upper_index:
		return search_signatures(file_bytes, lower_index, upper_index)
	else :
		return None

def search_extensions(extension, lower_index = 0, upper_index = len(extensions_list) - 1):
	index = math.floor((lower_index + upper_index) / 2)
	if extensions_list[index][0] == extension:
		#when found perform a localized search for all possibilities
		start = index
		end = index
		while extensions_list[start-1][0] == extension and start > 1:
			start-=1
		while extensions_list[end][0] == extension and end < len(extensions_list):
			end += 1
		if start!=end:
			return [mime[1] for mime in extensions_list[start: end]]
		else: return [extensions_list[start]]
	if  extensions_list[index][0] < extension:
		lower_index = index + 1
	elif extensions_list[index][0] > extension:
		upper_index = index - 1
	#Next check if lower_index == upper_index, which is the termination condition for the recursion
	if lower_index <= upper_index:
		return search_extensions(extension, lower_index, upper_index)
	else:
		return None

def identify_mime(filepath):
	extension = None
	if os.path.isfile(filepath) != True:
		return ['folder']
	if filepath.rfind('.') != -1 :
		extension = filepath[filepath.rfind('.') + 1:]
	x = search_extensions('zip')
	if extension == None:
		with open(filepath, 'br') as dafile:
			extension = search_signatures(dafile.read(128).hex())
	else:
		x = []
		x.append(extension)
		extension = x
	if extension != None:
		list = []
		for i in extension:
			x = search_extensions(i)
			if x != None:
				list.extend(x)
		if len(list) > 0:
			return list
		else:
			return ['unidentified','text/unidentified']
	else:
		return ['text/unidentified']

def identify(i):
	x = []
	if os.path.isfile(i):
		x.append((i, identify_mime(i)))
	elif os.path.isdir(i):
		for f in os.listdir(i):
			if i != './':
				x.extend(identify(i +'/'+ f))
			else:
				x.extend(identify(i+f))
	return x

def main():
	arguments = sys.argv
	arguments = arguments[1:]
	for i in arguments:
		if i=='-u' or i == '--update':
			update.download_signatures()
		elif os.path.exists(i):
			for x in identify(i):
				print(x)
		else:
			print('Argument not understood. Argument :',i)

if __name__ == '__main__':
	main()