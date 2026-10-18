# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/09_compare_two_strings.py
# Original location      :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/compare_strings.py   (last edited 2025-08-12)
# What this script does  :: Finds where two long strings start to differ.
# ----------------------------------------------------------------------------
a="0.9596916933508150789027631175771447405492376550528395118932519425998443191080142028789348609069064205585094732862753436045036916011624268985461933397148512720834852160504176541960806429188518899679310090947940803726651597065286795999799882667263378465744529350613015073395962831951341491186784574279020637367609667165614243117813772167021334699192348575061254668805421630395358079113066196441650390625"
b="0.959691693350815078902763117577144740549237655052839511893251942599844319108014202878934860906906420558509473286275343604638050206341288658673736233530070525610043781884226114612183748063096443854280067984933432014872438039679907786934571100310044178164419157296540679750587227247736075585248218202696132509902686709823840450659404253392319160994245615761765734580403553618464971753275893216883977696876042840878853341545457790308529948876693924485157138595564650997373286146743923778116493535363851565245186616570010142954589207036105811358747705382544445022975926607953682663836323067375012059200510861161531571738593517724609337202268958553621485202639999362000635379630633328494962069218151681341434162492475786945362203500014586789259989588531127572762508175165699613237888129715653035053640019779720628591797638022867611387258921626346736137997531582971009042263206042185968487327643646894616084515774155328214561244134099767806737523857473822926516845119274631497810486775069335940026776118192"

print(f"Length of a: {len(a)}")
print(f"Length of b: {len(b)}")
print()

# Find where they start to differ
min_len = min(len(a), len(b))
first_diff = -1
for i in range(min_len):
    if a[i] != b[i]:
        first_diff = i
        break

if first_diff == -1:
    print("Strings are identical up to the length of the shorter string")
    if len(a) != len(b):
        print(f"String a is longer by {len(a) - len(b)} characters")
else:
    print(f"First difference at position {first_diff}")
    print(f"Character in a: '{a[first_diff]}'")
    print(f"Character in b: '{b[first_diff]}'")
    print()
    
    # Show context around the difference
    start = max(0, first_diff - 10)
    end_a = min(len(a), first_diff + 10)
    end_b = min(len(b), first_diff + 10)
    
    print("Context around first difference:")
    print(f"a[{start}:{end_a}]: {a[start:end_a]}")
    print(f"b[{start}:{end_b}]: {b[start:end_b]}")
    print(" " * (first_diff - start) + "^")
    print()

# Count total differences
differences = 0
for i in range(min_len):
    if a[i] != b[i]:
        differences += 1

print(f"Total differences in overlapping part: {differences}")
print(f"Similarity percentage: {((min_len - differences) / min_len) * 100:.2f}%")

# Check if one is a prefix of the other
if len(a) > len(b) and a.startswith(b):
    print("String b is a prefix of string a")
elif len(b) > len(a) and b.startswith(a):
    print("String a is a prefix of string b")
