# bai 1
so = int(input("Check so chan le "))
if (so % 2 == 0):
    print("So chan ne")
else:
    print("So le ne")
# bai 2
a = int(input("Nhap so a "))
b = int(input("Nhap so b "))
c = int(input("Nhap so c "))

if (a + b > c and a + c > b and b + c > a):
    print("Do dai 3 canh cua tam giac")
else:
    print("Day kh phai la do dai 3 canh")

# bai 3
import time

x = time.localtime()
year = x[0]

age = int(input("Tinh nam sinh cua ban: "))
tinh_tuoi = year - age

print("Tuoi cua ban la " + str(tinh_tuoi))