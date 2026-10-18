# ----------------------------------------------------------------------------
# Prime research archive :: research/09-prime-matrix/day17-prime-matrix-eigenvalues/part2_prime_matrix_eigen.py
# Original location      :: research/09-prime-matrix/day17-prime-matrix-eigenvalues/part2.py   (last edited 2025-08-21)
# What this script does  :: Builds the N x N prime matrix and saves eigenvalues and eigenvectors.
# ----------------------------------------------------------------------------
import numpy as np

def is_prime(num):
    """
    Checks if a number is prime.
    A number is prime if it is greater than 1 and has no positive divisors other than 1 and itself.
    """
    if num <= 1:
        return False
    # Check for factors from 2 up to the square root of the number
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def create_prime_matrix(n):
    """
    Creates a square matrix of size n x n.
    It first generates a matrix with numbers from 1 to n^2.
    Then, it replaces any number that is not prime with 0.
    """
    # Create a matrix with numbers from 1 to n^2
    matrix = np.arange(1, n**2 + 1).reshape(n, n)
    
    # Create a new matrix of the same shape, initialized to zeros
    prime_matrix = np.zeros((n, n), dtype=int)
    
    # Iterate through each element of the original matrix
    for i in range(n):
        for j in range(n):
            # If the number is prime, place it in the new matrix
            if is_prime(matrix[i, j]):
                prime_matrix[i, j] = matrix[i, j]
                
    return prime_matrix

def get_eigen_properties(matrix):
    """
    Calculates the eigenvalues and eigenvectors of a given matrix.
    Uses the eig function from NumPy's linear algebra module.
    """
    # np.linalg.eig returns a tuple containing an array of eigenvalues
    # and a matrix where columns are the corresponding eigenvectors.
    eigenvalues, eigenvectors = np.linalg.eig(matrix)
    return eigenvalues, eigenvectors

# --- Main execution part of the script ---
if __name__ == '__main__':
    # Set the desired size of the matrix here.
    # For example, n = 4 will create a 4x4 matrix.
    n = int(input("Enter the value of N: "))

    output_lines = []
    output_lines.append(f"Generating a {n}x{n} prime matrix...\n")

    # 1. Create the prime matrix
    prime_matrix = create_prime_matrix(n)
    output_lines.append("--- Prime Matrix ---\n")
    print("\n--- Prime Matrix ---")
    print(prime_matrix)

    # Save the full prime matrix to a separate file for completeness
    np.savetxt("prime_matrix_full.txt", prime_matrix, fmt='%d', delimiter=', ')
    output_lines.append("(Full prime matrix saved in 'prime_matrix_full.txt')\n")

    # 2. Calculate its eigenvalues and eigenvectors
    eigenvalues, eigenvectors = get_eigen_properties(prime_matrix)

    # 3. Print the results
    output_lines.append("--- Eigenvalues ---\n")
    output_lines.append(str(np.round(eigenvalues, decimals=4)) + "\n")
    print("\n--- Eigenvalues ---")
    print(np.round(eigenvalues, decimals=4))

    output_lines.append("--- Eigenvectors ---\n")
    output_lines.append("Each column corresponds to an eigenvalue.\n")
    print("\n--- Eigenvectors ---")
    print("Each column corresponds to an eigenvalue.")
    print(np.round(eigenvectors, decimals=4))

    # Save the full eigenvectors to a separate file for completeness
    np.savetxt("prime_matrix_eigenvectors.txt", np.round(eigenvectors, decimals=4), fmt='%0.4f', delimiter=', ')
    output_lines.append("(Full eigenvectors saved in 'prime_matrix_eigenvectors.txt')\n")

    # Store results in a file
    with open("prime_matrix_results.txt", "w") as f:
        f.writelines(line if line.endswith("\n") else line + "\n" for line in output_lines)

