
def extract_page_num(f, suffix):
    num = ''
    if f[len(f)-(len(suffix)+1)] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
        num = f[len(f)-(len(suffix)+1)]
        if f[len(f)-(len(suffix)+2)] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            num = f[len(f)-(len(suffix)+2)] + num
    return num

print(extract_page_num("barley_p2_td.txt", "_td.txt"))
print(extract_page_num("barley_p12_td.txt", "_td.txt"))
