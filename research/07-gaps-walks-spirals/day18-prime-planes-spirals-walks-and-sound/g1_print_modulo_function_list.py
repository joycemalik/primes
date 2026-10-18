# ----------------------------------------------------------------------------
# Prime research archive :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/g1_print_modulo_function_list.py
# Original location      :: research/07-gaps-walks-spirals/day18-prime-planes-spirals-walks-and-sound/g1.py   (last edited 2025-08-24)
# What this script does  :: Prints the list of "x % i" functions used for the radial plots.
# ----------------------------------------------------------------------------
n=int(input("Enter a whole number n: "))
for i in range(1,n):
    print(f"\"x % {i}\",",)
