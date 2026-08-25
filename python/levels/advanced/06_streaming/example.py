def nonempty(lines):
    for line in lines:
        value = line.strip()
        if value: yield value
if __name__ == "__main__": print(list(nonempty([" alpha ", "", " beta"])))
