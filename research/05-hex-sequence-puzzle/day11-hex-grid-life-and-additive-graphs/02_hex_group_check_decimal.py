# ----------------------------------------------------------------------------
# Prime research archive :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/02_hex_group_check_decimal.py
# Original location      :: research/05-hex-sequence-puzzle/day11-hex-grid-life-and-additive-graphs/2.py   (last edited 2025-08-11)
# What this script does  :: The same check done in decimal arithmetic.
# ----------------------------------------------------------------------------
import re

def check_pattern_decimal(input_str: str):
    """
    Checks the sequence by performing all calculations in decimal,
    then converting the final result to hex for display.
    """
    print("--- Decimal Calculation Verification ---")
    
    # Clean the input string to ensure it only contains hex characters
    clean_str = re.sub(r'[^0-9a-fA-F]', '', input_str)
    
    if not clean_str:
        print("Input string is empty or contains no valid hex characters.")
        return

    print(f"Cleaned Sequence Length: {len(clean_str)} characters")
    print("-" * 40)

    # Define constants in DECIMAL for the calculation
    # These are the same numbers as before, just not in hex format.
    multiplier = 16843009      # This is 0x1010101
    modulus = 16777216         # This is 0x1000000
    addend = 1
    expected_result = 12345678 # This is 0xbc614e
    
    pass_count = 0
    fail_count = 0
    total_groups = 0

    # Process the string in 6-character groups
    for i in range(0, len(clean_str), 6):
        group_hex = clean_str[i:i+6]

        if len(group_hex) == 6:
            total_groups += 1
            # Convert the hex group to a standard decimal integer
            group_val_dec = int(group_hex, 16)

            # Perform the entire calculation using decimal numbers
            result_dec = (group_val_dec * multiplier + addend) % modulus
            
            # Compare the decimal result to the expected decimal result
            if result_dec == expected_result:
                status = "✅ PASSED"
                pass_count += 1
            else:
                status = "❌ FAILED"
                fail_count += 1
            
            # Print the detailed, readable output showing the decimal calculation
            print(f"Group {total_groups:02d} [{group_hex}]:")
            # The {:,} format adds commas to large numbers to make them readable
            print(f"  └─ Dec: ({group_val_dec:,} * {multiplier:,} + {addend}) % {modulus:,}")
            print(f"     └─ Result: {result_dec:,} (hex: {hex(result_dec)}) -> {status}")

    # Print the final summary
    print("-" * 40)
    print("--- Final Summary ---")
    print(f"Total 6-Character Groups Found: {total_groups}")
    print(f"✅ Checks Passed: {pass_count}")
    print(f"❌ Checks Failed: {fail_count}")
    print("-" * 40)

# --- EXAMPLE ---
# You can test this with any string. Here's a simple one.
test_input = "FA57A5123456"
check_pattern_decimal(test_input)