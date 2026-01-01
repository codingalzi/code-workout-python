def lc(file_name):
    count = 0
    with open(file_name, encoding='utf-8') as f:
        for line in f:
            count += 1
    return count
