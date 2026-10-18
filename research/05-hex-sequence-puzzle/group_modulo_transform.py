# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/group_modulo_transform.py
# Original location      :: learn/group_modulo_transform.py   (last edited 2025-08-11)
# What this script does  :: Group-and-modulo transform of the hex string.
# ----------------------------------------------------------------------------
"""
Group Modulo Transform Tester
============================

Applies the transformation (group_value × 16843009 + 1) mod 16777216 to each group
and prints the results in both decimal and hexadecimal.
"""

def group_modulo_transform(hex_sequence: str, group_size: int = 6, num_groups: int = 5):
    """Apply the transformation to the first few groups of the sequence."""
    groups = [hex_sequence[i:i+group_size] for i in range(0, len(hex_sequence), group_size)]
    print(f"Testing first {num_groups} groups of size {group_size}:")
    print(f"Transformation: (group_value × 16843009 + 1) mod 16777216")
    print(f"{'Group':>8} | {'Value':>10} | {'Transformed':>10} | {'Hex':>8}")
    print('-'*50)
    for idx, group in enumerate(groups[:num_groups]):
        if len(group) != group_size:
            continue
        value = int(group, 16)
        transformed = (value * 16843009 + 1) % 16777216
        print(f"{group:>8} | {value:10} | {transformed:10} | 0x{transformed:06X}")

def main():
    hex_sequence = "FA57A5BA4F24D856A1F1EA15A532475CA4AA4981BA47849A354A54A5E17A1621984A25924481F8E24749845245258A1B81B47A4A3215216A588CA578552188EA4B1FA121AA4924DA544EE8325A4E112145F852381A4E25C82AF83853218621C21C25681A555BA5245846219A58384124C25EA4B81924485386251844A4486A181924958A8814E51A49F185AA168138142284F95CA5C13246252875984AD86232432494DA16487A585AB1CAE41D813A13A44C8422583552324E2C52521CA52A12B29EA161158A8725C24AA13894585A4249848471A14A22415A4E5BD278514A211285F8A2154B8215258A5D814268254184624A8112132122C25944A54815A42A5A845818211943A518484A1A81B8638132E214A12845C855251A482488AD94424B846224C13818252D4D844A4D816A1618A82592461E824A124E258468122858A8D2152459188172A247582A4C8A165125C2221C8E5A49A4A552182681D8742A211A18538B841A4651258A5814432924B552A1F7A511A4141AA1A1C8481AAC51258AD165A1942C"
    group_modulo_transform(hex_sequence, group_size=6, num_groups=5)

if __name__ == "__main__":
    main()
