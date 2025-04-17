def parser(arr,f):
    lines = f.readlines()
    current_arr = [0, [], ""]
    for line in lines:
        line = line.strip()
        k = 0
        if line.endswith("?"):
            current_arr[0] = line.split(". ")[1]
        elif line.startswith(tuple("12345")):
            current_arr[1].append(line.split(". ")[1])
        elif line.startswith("Ответ: "):
            answer = line.split(": ")[1]
            current_arr[2] = current_arr[1][int(answer)-1]
            arr.append(current_arr)
            current_arr = [0, [], ""]
    return