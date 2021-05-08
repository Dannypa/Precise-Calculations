import math


def lcm(a: int, b: int) -> int:
    return a * b // math.gcd(a, b)


def list_to_int(a: list) -> int:
    if len(a) == 0:
        return 0
    return int(''.join(a))


def is_number(a: str):
    digits = set("1234567890")
    for i in a:
        if i not in digits:
            return False
    return True


class UFraction:
    out_format = 0  # 0 is for {numerator/denominator}, 1 is for {INTEGER_PART numerator/denominator}

    # only numbers for now
    def __init__(self, numerator=0.0, denominator=1.0, to_reduce=True):
        if type(numerator) not in {float, int} or type(denominator) not in {float, int}:
            raise ValueError("Arguments must be float or int")
        if denominator == 0:
            raise ZeroDivisionError("<<explanation>>")
        while numerator % 1 != 0 or denominator % 1 != 0:
            numerator *= 10
            denominator *= 10
        if denominator < 0:
            numerator *= -1
            denominator *= -1
        self.numerator = int(numerator)
        self.denominator = int(denominator)
        if not to_reduce:
            return
        cur_gcd = math.gcd(self.numerator, self.denominator)
        self.numerator //= cur_gcd
        self.denominator //= cur_gcd

    def __repr__(self):
        return f"Upgraded fraction, numerator = {self.numerator}, denominator = {self.denominator}"

    def __str__(self):
        if self.numerator % self.denominator == 0:
            return str(int(self.numerator / self.denominator))
        if self.out_format == 1:
            integer_part = self.numerator // self.denominator
            if integer_part != 0:
                return f"{integer_part} and {self.numerator - self.denominator * integer_part}/{self.denominator}"
        return f"{self.numerator}/{self.denominator}"

    def __eq__(self, other):
        to_comp = other
        if type(other) != UFraction:
            to_comp = UFraction(other)
        return self.denominator == to_comp.denominator and self.numerator == to_comp.numerator

    def __add__(self, other):
        to_add = other
        if type(other) != UFraction:
            to_add = UFraction(other)
        cur_numerator = self.numerator
        cur_denominator = self.denominator
        new_denominator = lcm(cur_denominator, to_add.denominator)
        cur_numerator = (
                new_denominator * cur_numerator / cur_denominator +
                to_add.numerator * new_denominator / to_add.denominator
        )
        cur_denominator = new_denominator
        return UFraction(cur_numerator, cur_denominator)

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        to_mul = other
        if type(other) != UFraction:
            to_mul = UFraction(other)
        return UFraction(self.numerator * to_mul.numerator, self.denominator * to_mul.denominator)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __neg__(self):
        return UFraction(-self.numerator, self.denominator)

    def __sub__(self, other):
        return self + other.__neg__()

    def __rsub__(self, other):
        return other + self.__neg__()

    def __truediv__(self, other):
        to_div = other
        if type(other) != UFraction:
            to_div = UFraction(other)
        return self * UFraction(to_div.denominator, to_div.numerator)

    def __rtruediv__(self, other):
        return UFraction(other * self.denominator, self.numerator)

    def __pow__(self, power, modulo=None):
        to_power = power
        if type(to_power) == UFraction:
            to_power = to_power.execute()  # TODO: may be precise calc if rt is done
        if to_power < 0:
            to_power *= -1
            self.numerator, self.denominator = self.denominator, self.numerator
        return UFraction(self.numerator ** to_power, self.denominator ** to_power)

    def __rpow__(self, other):
        return other ** self.execute()  # TODO: same as pow

    def __lt__(self, other):
        to_comp = other
        if type(other) != UFraction:
            to_comp = UFraction(other)
        return (self - to_comp).numerator < 0

    def __gt__(self, other):
        to_comp = other
        if type(other) != UFraction:
            to_comp = UFraction(other)
        return (self - to_comp).numerator > 0

    def __le__(self, other):
        to_comp = other
        if type(other) != UFraction:
            to_comp = UFraction(other)
        return (self - to_comp).numerator <= 0

    def __ge__(self, other):
        to_comp = other
        if type(other) != UFraction:
            to_comp = UFraction(other)
        return (self - to_comp).numerator >= 0

    def execute(self):
        return self.numerator / self.denominator

    def __abs__(self):
        return UFraction(abs(self.numerator), self.denominator)

    @staticmethod
    def convert_from_periodic(a):
        if type(a) != str:
            raise ValueError("Argument must be a str")
        before_dot = []  # the integer part
        before_parenthesis = []
        in_parenthesis = []
        i = 0
        while i < len(a):
            if a[i] == '.':
                break
            before_dot.append(a[i])
            i += 1
        i += 1
        while i < len(a):
            if a[i] == '(':
                break
            before_parenthesis.append(a[i])
            i += 1
        i += 1
        while i < len(a):
            if a[i] == ')':
                break
            in_parenthesis.append(a[i])
            i += 1
        int_before_dot = list_to_int(before_dot)
        int_before_parenthesis = list_to_int(before_parenthesis)
        if len(in_parenthesis) == 0:
            return UFraction(int_before_parenthesis + int_before_dot * 10 ** len(before_parenthesis),
                             10 ** len(before_parenthesis))
        after_dot = before_parenthesis.copy()
        after_dot.extend(in_parenthesis)
        cur_numerator = list_to_int(after_dot) - int_before_parenthesis + int_before_dot * (
                    10 ** (len(before_parenthesis))) * (10 ** (len(in_parenthesis)) - 1)
        cur_denominator = 10 ** (len(before_parenthesis)) * (10 ** (len(in_parenthesis)) - 1)
        return UFraction(cur_numerator, cur_denominator)

    @staticmethod
    def from_string(inp: str):
        inp = inp.replace(' ', '')
        if inp.count("and") == 1:
            integral, fractional = inp.split("and")
            if not is_number(integral):
                raise ValueError
            integral = int(integral)
            fractional_res = UFraction.from_string(fractional)
            if fractional_res >= 1:
                raise ValueError
            return UFraction(integral) + fractional_res
        elif inp.count('/') == 1:
            numerator, denominator = inp.split('/')
            if not is_number(numerator) or not is_number(denominator):
                raise ValueError
            numerator = int(numerator)
            denominator = int(denominator)
            return UFraction(numerator, denominator)
        else:
            raise ValueError

    @classmethod
    def set_out_format(cls, new_format):
        cls.out_format = new_format


if __name__ == '__main__':
    print(UFraction(1, 2) ** (-1))
