import time
import sys

# Meningkatkan batas rekursi untuk pengujian iteratif angka besar (opsional, tapi aman dilakukan)
sys.setrecursionlimit(20000)

class FibonacciAnalyzer:
    def __init__(self):
        pass

    def recursive_naive(self, n):
        """
        Pendekatan Rekursif Naif.
        Kompleksitas: O(2^n) - Eksponensial.
        Sangat lambat untuk n > 35.
        """
        if n <= 1:
            return n
        return self.recursive_naive(n-1) + self.recursive_naive(n-2)

    def iterative(self, n):
        """
        Pendekatan Iteratif.
        Kompleksitas: O(n) - Linear.
        Sangat cepat bahkan untuk n = 10000.
        """
        if n <= 1:
            return n
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    def measure_time(self, algorithm_func, n):
        """
        Mengukur waktu eksekusi fungsi dalam detik.
        """
        start_time = time.perf_counter()
        result = algorithm_func(n)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        return result, execution_time