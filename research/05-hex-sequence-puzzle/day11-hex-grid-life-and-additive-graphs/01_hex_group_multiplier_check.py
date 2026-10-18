# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/01_hex_group_multiplier_check.py
# Original location      :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/1.py   (last edited 2025-08-11)
# What this script does  :: Checks 6-digit hex groups: g * 0x1010101 mod 2^24 == 0xBC614E (matches 0 of 130).
# ----------------------------------------------------------------------------
import re

def check_pattern(input_str: str):
    """
    Cleans and checks any string against the correct pattern.
    """
    print("--- Starting Verification ---")
    
    # Clean the string to keep only valid hexadecimal characters (0-9, a-f, A-F)
    clean_str = re.sub(r'[^0-9a-fA-F]', '', input_str)
    
    if not clean_str:
        print("Input string is empty or contains no valid hex characters. Exiting.")
        return

    print(f"Cleaned Sequence Length: {len(clean_str)} characters")
    print("-" * 30)

    # --- CORE LOGIC: Ensure these constants are exactly correct ---
    multiplier =      0x1010101
    modulus =         0x1000000
    expected_result = 0xbc614e
    # -----------------------------------------------------------
    
    pass_count = 0
    fail_count = 0
    total_groups = 0

    # Iterate through the string in 6-character steps
    for i in range(0, len(clean_str), 6):
        group_hex = clean_str[i:i+6]

        if len(group_hex) == 6:
            total_groups += 1
            group_val = int(group_hex, 16)
            
            # Apply the correct formula
            result = (group_val * multiplier + 1) % modulus
            
            if result == expected_result:
                status = "✅ PASSED"
                pass_count += 1
            else:
                status = "❌ FAILED"
                fail_count += 1
            
            print(f"Group {total_groups:02d} [{group_hex}]: Calculated Result = {hex(result):<9} -> {status}")

    print("-" * 30)
    print("--- Final Summary ---")
    print(f"Total 6-Character Groups Found: {total_groups}")
    print(f"✅ Checks Passed: {pass_count}")
    print(f"❌ Checks Failed: {fail_count}")
    print("-" * 30)

# --- EXAMPLE USAGE ---

# This is the original 510-character sequence where the pattern should pass for all 85 groups.
original_puzzle_sequence = (
    "FA57A5BA4F24D856A1F1EA15A532475CA4AA4981BA47849A354A54A5E17A1621984A25"
    "924481F8E24749845245258A1B81B47A4A3215216A588CA578552188EA4B1FA121AA4"
    "924DA544EE8325A4E112145F852381A4E25C82AF83853218621C21C25681A555BA524"
    "5846219A58384124C25EA4B81924485386251844A4486A181924958A8814E51A49F18"
    "5AA168138142284F95CA5C13246252875984AD86232432494DA16487A585AB1CAE41D"
    "813A13A44C8422583552324E2C52521CA52A12B29EA161158A8725C24AA13894585A4"
    "249848471A14A22415A4E5BD278514A211285F8A2154B8215258A5D81426825418462"
    "4A8112132122C25944A54815A42A5A845818211943A518484A1A81B8638132E214A12"
    "845C855251A482488AD94424B846224C13818252D4D844A4D816A1618A82592461E82"
    "4A124E258468122858A8D2152459188172A247582A4C8A165125C2221C8E5A49A4A55"
    "2182681D8742A211A18538B841A4651258A5814432924B552A1F7A511A4141AA1A1C8"
    "481AAC51258AD165A1942C"
)

check_pattern(original_puzzle_sequence)