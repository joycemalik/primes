# ----------------------------------------------------------------------------
# Prime research archive :: research/08-machine-learning/gpu_prime_acceleration_test.py
# Original location      :: learn/gpu test.py   (last edited 2025-08-04)
# What this script does  :: RTX 4060 GPU prime sieve and batch test.
# ----------------------------------------------------------------------------
# === FIXED RTX 4060 GPU PRIME ACCELERATION ===
# Clean, working GPU acceleration for massive prime detection!

import torch
import numpy as np
import time
import math
import matplotlib.pyplot as plt

print("🔥🔥🔥 RTX 4060 GPU ACCELERATION SYSTEM 🔥🔥🔥")

# Check CUDA availability
GPU_AVAILABLE = False
device = torch.device("cpu")

try:
    if torch.cuda.is_available():
        device = torch.device("cuda")
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        
        print(f"🚀 GPU DETECTED: {gpu_name}")
        print(f"🔥 GPU Memory: {gpu_memory:.1f} GB")
        print(f"⚡ Estimated CUDA Cores: ~3072 (RTX 4060)")
        print(f"🎯 Device: {device}")
        
        GPU_AVAILABLE = True
        
        # Test GPU with a simple operation
        test_tensor = torch.tensor([1, 2, 3], device=device)
        print(f"✅ GPU test successful: {test_tensor.sum().item()}")
        
    else:
        print("❌ CUDA not available!")
        
except Exception as e:
    print(f"⚠️ GPU initialization failed: {e}")
    print("🔄 Falling back to CPU mode")

class RTX4060PrimeGPU:
    """
    RTX 4060 GPU-accelerated prime detection system
    Clean, efficient, and error-free!
    """
    
    def __init__(self):
        self.device = device
        self.gpu_available = GPU_AVAILABLE
        self.batch_size = 100000  # Process 100K numbers at a time
        
        print(f"🔧 Prime GPU System initialized:")
        print(f"   GPU Available: {self.gpu_available}")
        print(f"   Device: {self.device}")
        print(f"   Batch size: {self.batch_size:,}")
    
    def is_prime_single(self, n):
        """Check if a single number is prime (CPU)"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def gpu_prime_sieve(self, limit):
        """
        GPU-accelerated Sieve of Eratosthenes
        """
        if not self.gpu_available or limit < 1000:
            return self.cpu_prime_sieve(limit)
        
        try:
            print(f"🔥 GPU Sieve processing up to {limit:,}...")
            
            # Create sieve array on GPU
            sieve = torch.ones(limit + 1, dtype=torch.bool, device=self.device)
            sieve[0] = False
            if limit >= 1:
                sieve[1] = False
            
            # Mark multiples as composite
            sqrt_limit = int(math.sqrt(limit)) + 1
            
            for p in range(2, sqrt_limit):
                if p >= len(sieve):
                    break
                    
                if sieve[p].item():
                    # Mark multiples of p starting from p^2
                    start = p * p
                    if start <= limit:
                        # Create indices for multiples
                        multiples = torch.arange(start, limit + 1, p, device=self.device)
                        if len(multiples) > 0:
                            sieve[multiples] = False
            
            # Extract prime indices
            prime_indices = torch.nonzero(sieve, as_tuple=False).flatten()
            primes = prime_indices.cpu().numpy()
            
            print(f"✅ GPU Sieve found {len(primes):,} primes")
            return primes.tolist()
            
        except Exception as e:
            print(f"⚠️ GPU sieve failed: {e}")
            print("🔄 Falling back to CPU sieve")
            return self.cpu_prime_sieve(limit)
    
    def cpu_prime_sieve(self, limit):
        """CPU Sieve of Eratosthenes fallback"""
        print(f"💻 CPU Sieve processing up to {limit:,}...")
        
        if limit < 2:
            return []
        
        sieve = np.ones(limit + 1, dtype=bool)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(math.sqrt(limit)) + 1):
            if sieve[i]:
                sieve[i*i::i] = False
        
        primes = np.where(sieve)[0].tolist()
        print(f"✅ CPU Sieve found {len(primes):,} primes")
        return primes
    
    def gpu_batch_primality_test(self, numbers):
        """
        GPU batch primality testing
        """
        if not self.gpu_available:
            return [self.is_prime_single(n) for n in numbers]
        
        try:
            # Convert to GPU tensor
            nums_gpu = torch.tensor(numbers, dtype=torch.int64, device=self.device)
            results = torch.zeros(len(numbers), dtype=torch.bool, device=self.device)
            
            # Handle small numbers
            results[nums_gpu == 2] = True
            results[nums_gpu < 2] = False
            
            # Handle even numbers
            even_mask = (nums_gpu % 2 == 0) & (nums_gpu > 2)
            results[even_mask] = False
            
            # Check odd numbers > 2
            odd_mask = (nums_gpu % 2 == 1) & (nums_gpu > 2)
            odd_numbers = nums_gpu[odd_mask]
            
            if len(odd_numbers) > 0:
                odd_results = torch.ones(len(odd_numbers), dtype=torch.bool, device=self.device)
                
                # Check divisibility for each odd number
                max_num = torch.max(odd_numbers).item()
                max_divisor = int(math.sqrt(max_num)) + 1
                
                for div in range(3, max_divisor + 1, 2):
                    if div > max_num:
                        break
                    divisible = (odd_numbers % div == 0)
                    odd_results[divisible] = False
                
                results[odd_mask] = odd_results
            
            return results.cpu().numpy().tolist()
            
        except Exception as e:
            print(f"⚠️ GPU batch test failed: {e}")
            return [self.is_prime_single(n) for n in numbers]
    
    def massive_prime_hunt(self, start, end):
        """
        MASSIVE prime detection with automatic GPU/CPU selection
        """
        print(f"\n🚀 MASSIVE PRIME HUNT INITIATED! 🚀")
        print(f"Range: [{start:,}, {end:,}]")
        print(f"Range size: {end-start+1:,} numbers")
        
        start_time = time.time()
        
        # Choose method based on range
        if start == 2 and end <= 50_000_000:  # Use sieve for ranges starting from 2
            primes = self.gpu_prime_sieve(end)
        else:
            # Use batch processing for custom ranges
            all_primes = []
            current = start
            
            while current <= end:
                batch_end = min(current + self.batch_size - 1, end)
                batch_numbers = list(range(current, batch_end + 1))
                
                # Process batch
                batch_results = self.gpu_batch_primality_test(batch_numbers)
                
                # Extract primes
                batch_primes = [num for num, is_prime in zip(batch_numbers, batch_results) if is_prime]
                all_primes.extend(batch_primes)
                
                # Progress update
                progress = (batch_end - start + 1) / (end - start + 1) * 100
                print(f"   Progress: {progress:.1f}% | Primes found: {len(all_primes):,}")
                
                current = batch_end + 1
            
            primes = all_primes
        
        detection_time = time.time() - start_time
        
        print(f"\n🎯 MASSIVE PRIME HUNT COMPLETE!")
        print(f"⏱️  Detection time: {detection_time:.2f} seconds")
        print(f"🔢 Primes found: {len(primes):,}")
        
        if detection_time > 0:
            print(f"🚀 Speed: {len(primes)/detection_time:.0f} primes/second")
        
        print(f"📊 Prime density: {len(primes)/(end-start+1)*100:.4f}%")
        
        # Show some results
        if primes:
            print(f"\n📈 Results:")
            print(f"   Smallest prime: {min(primes):,}")
            print(f"   Largest prime: {max(primes):,}")
            
            if len(primes) >= 5:
                print(f"   Last 5 primes: {primes[-5:]}")
        
        return primes
    
    def benchmark_performance(self):
        """Run performance benchmarks"""
        print(f"\n� PERFORMANCE BENCHMARK 🏁")
        
        test_ranges = [
            ("Small: 10K", 2, 10_000),
            ("Medium: 100K", 2, 100_000),
            ("Large: 1M", 2, 1_000_000),
        ]
        
        results = []
        
        for name, start, end in test_ranges:
            print(f"\n🔥 Testing {name}...")
            
            start_time = time.time()
            primes = self.massive_prime_hunt(start, end)
            end_time = time.time()
            
            duration = end_time - start_time
            speed = len(primes) / duration if duration > 0 else 0
            
            results.append({
                'name': name,
                'primes': len(primes),
                'time': duration,
                'speed': speed
            })
            
            print(f"   ✅ {name}: {len(primes):,} primes in {duration:.2f}s ({speed:.0f} primes/s)")
        
        return results

# Initialize the system
print("🔧 Initializing RTX 4060 Prime GPU System...")
rtx_prime = RTX4060PrimeGPU()

# Run a quick test
print("\n🔥 QUICK GPU TEST")
if rtx_prime.gpu_available:
    test_primes = rtx_prime.massive_prime_hunt(2, 10000)
    print(f"🎯 Quick test: Found {len(test_primes):,} primes in range [2, 10000]")
else:
    print("💻 Running in CPU mode")
    test_primes = rtx_prime.massive_prime_hunt(2, 1000)
    print(f"🎯 CPU test: Found {len(test_primes):,} primes in range [2, 1000]")

print("✅ System ready for massive prime hunting!")