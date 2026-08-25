import argparse

def parser():
    value = argparse.ArgumentParser()
    value.add_argument("--minutes", type=int, default=25)
    return value

def run(minutes): return f"Study for {minutes} minutes"
if __name__ == "__main__": print(run(parser().parse_args().minutes))
