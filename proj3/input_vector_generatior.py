import sys
def append_vectors(S):
    for index in range(len(S)):
        if S[index] == "X":
            append_vectors(S[0:index]+'1'+S[index+1:])
            append_vectors(S[0:index]+'0'+S[index+1:])
            return
    print(S)
    return

if __name__ == "__main__":
    f = open(sys.argv[1])
    lines = f.readlines()
    S = lines[2].split()[3]
    append_vectors(S)