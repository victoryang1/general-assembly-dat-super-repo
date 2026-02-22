1. Chipotle data exploration
	* Columns
		1. The first column appears to be an order ID, which probably represents a single unique transaction made up of one or more items
		2. The second column appears to be the quantity of the item purchased for that order
		3. The third column appears to be the name of the item
		4. The fourth column appears to be an optional field that further describes the item
		5. The fifth column appears to be price for that quantity of items
	* Rows
		1. Each row appears to be an item of an order
		
	```head -n5 chipotle.tsv```
2. There appear to be 1834 orders

	```
	tail -n1 chipotle.tsv
	cut -f1,1 chipotle.tsv | uniq | wc -l
	```
3. There are 4623 lines

	```wc -l chipotle.tsv```
4. There are more individual orders for chicken than steak.

	```
	grep -ic "chicken burrito" chipotle.tsv
	grep -ic "steak burrito" chipotle.tsv
	```
5. Chicken burritos more often have black beans.

	```
	grep -i "chicken burrito" chipotle.tsv | grep -ic "black"
	grep -i "chicken burrito" chipotle.tsv | grep -ic "pinto"
	```
6. Use find to find files...

	```find . -name *.?sv```
7. Assumes only one instance of the word per line

	```grep -ir 'dictionary' . | wc -l```

8. Of the 1834 orders, 1599 of them contain chicken or steak.

	```grep -i "chicken\|steak" data/chipotle.tsv | cut -f1,1 | uniq | wc -l```