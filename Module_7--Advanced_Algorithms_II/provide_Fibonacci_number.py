mem = {}

def provide_Fibonacci_number(n):
    if n <= 1:
        return 1
    if mem.get(n, -1) != -1:
        return mem[n]
    output = provide_Fibonacci_number(n - 1) + provide_Fibonacci_number(n - 2)
    mem[n] = output
    return output

if __name__ == "__main__":
    for i in range(0, 10):
        print(provide_Fibonacci_number(i))