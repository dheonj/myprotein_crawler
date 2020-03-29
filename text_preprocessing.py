import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8-sig')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8-sig')

location="C:\\Users\\jeong\\Documents\\github\\myprotein_crawler\\raw_data_kor_updated.txt"
file = open(location, 'r',encoding = 'utf-8-sig')
categories=[]
category_size=[]
products=[]


class supplement:
    count = 0  # 클래스 변수

    def __init__(self, width, height):
        self.name = width
        self.serving = height
        supplement.count += 1

for index, line in enumerate(file):
    line=line.strip()
    if line!="\n" or bool(line):
        if line[-7:]=="results":
            categories.append(index)
            category_size.append(int(line[:-8]))
        else:
            if line[0:7]=='PRODUCT':
                products.append([])
                products[len(products)-1].append(line[12:].strip())
            elif line[0:7]=='SERVING' or line[0:7]=='NUTINFO':
                products[len(products)-1].append(line)
                pass
            else:
                pass
            # print(line)

print(sum(category_size))

file.close()
