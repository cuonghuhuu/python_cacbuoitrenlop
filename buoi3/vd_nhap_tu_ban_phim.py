a = int(input("Nhap so a "))
b = int(input("Nhap so b "))

tinh_tong = a + b

print("Tong a va b la ", tinh_tong)

# bai 2
your_name = str(input("Ten cua ban la "))
job = str(input("Cong viec cua ban "))

print("Ban la " + str(your_name), (" cong viec cua toi ") + str(job))

# bai 3
so_thu_1 = int(input("Nhap so nguyen thu 1 "))
so_thu_2 = int(input("Nhap so nguyen thu 2 "))
so_thu_3 = int(input("Nhap so nguyen thu 3 "))

tinh_tong_3_so = so_thu_1 + so_thu_2 + so_thu_3
tinh_trung_binh = tinh_tong_3_so / 3

print("Tong cua 3 so la ", tinh_tong_3_so)
print("Trung binh cong cua 3 so la ", tinh_trung_binh)

tinh_hieu_1_2 = so_thu_1 - so_thu_2
tinh_hieu_1_3 = so_thu_1 - so_thu_3
tinh_hieu_2_3 = so_thu_2 - so_thu_3

print("Hieu cua so thu 1 va so thu 2 la ", tinh_hieu_1_2)
print("Hieu cua so thu 1 va so thu 3 la ", tinh_hieu_1_3)
print("Hieu cua so thu 2 va so thu 3 la ", tinh_hieu_2_3)

chia_lay_phan_nguyen = so_thu_1 // so_thu_2
chia_lay_phan_du = so_thu_1 % so_thu_2
chia_chinh_xac = so_thu_1 / so_thu_2

print("So thu 1 chia lay phan nguyen cho so thu 2 la ", chia_lay_phan_nguyen)
print("So thu 1 chia lay phan du cho so thu 2 la ", chia_lay_phan_du)
print("So thu 1 chia chinh xac cho so thu 2 la ", chia_chinh_xac)

# bai 4
chuoi_1 = str(input("Nhap chuoi thu 1 "))
chuoi_2 = str(input("Nhap chuoi thu 2 "))
chuoi_3 = str(input("Nhap chuoi thu 3 "))

ghep_3_chuoi = chuoi_1 + " " + chuoi_2 + " " + chuoi_3

print("Chuoi sau khi ghep la ", ghep_3_chuoi)

# bai 5
pi = 3.14
ban_kinh = float(input("Nhap ban kinh hinh tron "))

chu_vi_hinh_tron = 2 * ban_kinh * pi
dien_tich_hinh_tron = pi * ban_kinh * ban_kinh

print("Chu vi hinh tron la ", chu_vi_hinh_tron)
print("Dien tich hinh tron la ", dien_tich_hinh_tron)
