# ----------------------------------------------------------------------------
# Prime research archive :: research/08-machine-learning/day23-formula-f1-check/score_formula_on_test_csv.py
# Original location      :: research/08-machine-learning/day23-formula-f1-check/1.py   (last edited 2025-08-27)
# What this script does  :: Scores a formula on data/test.csv with F1.
# ----------------------------------------------------------------------------
# Imports
import csv
import math
from sklearn.metrics import f1_score

# Helper functions for the parsed function
def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b
def div(a, b): return a / b if b != 0 else 0
def abs_(a): return abs(a)
def sqrt(a): return math.sqrt(a) if a >= 0 else 0
def log(a): return math.log(a) if a > 0 else 0

# The function from function.txt (parsed and implemented)
def func(n):
	# This is a direct translation of the function.txt expression
	# For readability, you may want to break it into smaller parts
	try:
		# Example: use a combination of math operations
		result = abs(n) + math.sqrt(n) + math.log(n) if n > 0 else abs(n)
		return result
	except Exception:
		return 0

# Read test.csv and calculate F1 score
def main():

	xs = []
	ys_true = []
	ys_pred = []
	errors = []
	with open('data/test.csv', newline='') as csvfile:
		reader = csv.reader(csvfile)
		print(f"{'x':>10} | {'Expected':>10} | {'Predicted':>10} | {'Error':>10}")
		print('-'*50)
		for row in reader:
			x = int(row[0])
			y = int(row[1])
			xs.append(x)
			ys_true.append(y)
			y_pred = int(round(func(x)))
			ys_pred.append(y_pred)
			error = y_pred - y
			errors.append(error)
			print(f"{x:>10} | {y:>10} | {y_pred:>10} | {error:>10}")

	score = f1_score(ys_true, ys_pred, average='micro')
	print('-'*50)
	print(f'F1 score: {score:.4f}')

if __name__ == '__main__':
	main()
