#removes every duplicate line in a file
def removedupes(file):
    
    with open(file, 'r') as f:
        lines = f.readlines()
    b4 = len(lines)

    lines = list(set(lines))
    lines = [line for line in lines if line.startswith("discord.gg/")]
    with open(file, 'w') as f:
        f.writelines(lines)

    print(f"removed {b4 - len(lines)} duplicates")
removedupes("invites.txt")
