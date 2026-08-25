from cProfile import Profile

def workload(): return sum(i * i for i in range(10000))
if __name__ == "__main__":
    with Profile() as profile: print(workload())
    profile.print_stats(sort="cumulative")
