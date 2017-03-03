def multiple(a, b):
    """Return the smallest number n that is a multiple of both a and b.

    >>> multiple(3, 4)
    12
    >>> multiple(14, 21)
    42
    """
    lcm = max(a,b)
    while lcm % min(a,b) != 0:
        lcm = lcm + max(b,a)
    return lcm


def unique_digits(n):
    """Return the number of unique digits in positive integer n

    >>> unique_digits(8675309) # All are unique
    7
    >>> unique_digits(1313131) # 1 and 3
    2
    >>> unique_digits(13173131) # 1, 3, and 7
    3
    >>> unique_digits(10000) # 0 and 1
    2
    >>> unique_digits(101) # 0 and 1
    2
    >>> unique_digits(10) # 0 and 1
    2
    """
    def has_digit(n,k):
        check= False
        while n > 0:
            digit = n%10
            if digit == k:
                check = True
            n=n//10
        return check
    b = 0
    unique = 0
    while b < 10:
        if has_digit(n,b):
            unique +=1
            b+=1
        else:
            b+=1
    return unique