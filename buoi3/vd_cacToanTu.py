class ToanTuDemo:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def phep_toan_so_hoc(self):
        print("=== CAC PHEP TOAN SO HOC ===")
        print(f"a + b + c = {self.a + self.b + self.c}")
        print(f"a - b - c = {self.a - self.b - self.c}")
        print(f"a * b * c = {self.a * self.b * self.c}")
        print(f"a / b = {self.a / self.b}")
        print(f"a / c = {self.a / self.c}")
        print(f"a ** b = {self.a ** self.b}")
        print(f"b ** c = {self.b ** self.c}")

    def toan_tu_quan_he(self):
        print("\n=== TOAN TU QUAN HE ===")
        print(f"a > b: {self.a > self.b}")
        print(f"a < b: {self.a < self.b}")
        print(f"a == b: {self.a == self.b}")
        print(f"a != c: {self.a != self.c}")
        print(f"b <= c: {self.b <= self.c}")
        print(f"a >= c: {self.a >= self.c}")

    def toan_tu_gan(self):
        print("\n=== TOAN TU GAN ===")

        x = self.a
        x += self.b
        print(f"Sau x += b: {x}")

        y = self.a
        y *= self.c
        print(f"Sau y *= c: {y}")

        z = self.a
        z /= self.b
        print(f"Sau z /= b: {z}")

        t = self.a
        t -= self.c
        print(f"Sau t -= c: {t}")

    def toan_tu_logic(self):
        print("\n=== TOAN TU LOGIC ===")
        print(f"(a > b) and (c > b): {(self.a > self.b) and (self.c > self.b)}")
        print(f"(a < b) or (c > b): {(self.a < self.b) or (self.c > self.b)}")
        print(f"not (a == b): {not (self.a == self.b)}")

    def toan_tu_bit(self):
        print("\n=== TOAN TU THAO TAC BIT ===")
        print(f"a & b = {self.a & self.b}")
        print(f"a | b = {self.a | self.b}")
        print(f"~a = {~self.a}")
        print(f"a ^ c = {self.a ^ self.c}")
        print(f"a << 3 = {self.a << 3}")
        print(f"a >> 2 = {self.a >> 2}")

    def hien_thi_tat_ca(self):
        self.phep_toan_so_hoc()
        self.toan_tu_quan_he()
        self.toan_tu_gan()
        self.toan_tu_logic()
        self.toan_tu_bit()


if __name__ == "__main__":
    demo = ToanTuDemo(16, 3, 5)
    demo.hien_thi_tat_ca()
