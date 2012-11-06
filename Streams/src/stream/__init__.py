import random
import sys
import math

# Abstract Stream
class Stream(object):
    def __init__(self):
        pass

    def __iter__(self):
        yield self.popNext()
        yield lambda: self

    def popNext(self):
        raise NotImplementedError("Should have implemented this method")

    def popN(self,num_N):
        raise NotImplementedError("Should have implemented this method")

class Primes(Stream):
    def __init__(self):
        super(Primes, self).__init__()
        self.last_send_prime = 1

    def popNext(self):
        a = self.last_send_prime + 1;
        while True:
            if self.isprime(a):
                self.last_send_prime = a
                return a
            else:
                a += 1

    def isprime(self, num):
        num *= 1.0
        for divisor in range(2,int(num**0.5)+1):
            if num/divisor==int(num/divisor):
                return False
        return True

    def popN(self,num_N):
        n_poped_list = ()
        while(num_N):
            n_poped_list.add(self.popNext())
            num_N -= 1
        return n_poped_list



class Randoms(Stream):
    def __init__(self):
        super(Randoms, self).__init__()
        self.randoms = set()

    def popNext(self):
        rand_val = 0
        while True:
            rand_val = random.randint(1,100000)
            if rand_val not in self.randoms:
                break
        self.randoms.add(rand_val)
        return rand_val

    def popN(self,num_N):
        n_poped_set = set()
        while num_N:
            n_poped_set.add(self.popNext())
            num_N -= 1
        return n_poped_set

class PrimeFactors(Stream):
    def __init__(self, val):
        super(PrimeFactors, self).__init__()
        self.val = val
        self.factors = []
        self.stream_send_factors = []

    def popNext(self):
        if not self.factors:
            self.prime_factorize(self.val)

        for factor in self.factors:
            if factor not in self.stream_send_factors:
                self.stream_send_factors.append(factor)
                return factor

        return None

    def popN(self,num_N):
        n_poped_list = ()
        while num_N:
            n_poped_list.add(self.popNext())
            num_N -= 1
        return n_poped_list

    def prime_factorize(self, n):
        number = math.fabs(n)
        while number > 1:
            factor = self.get_next_prime_factor(number)
            self.factors.append(factor)
            number /= factor
        if n < -1:
            self.factors[0] = -self.factors[0]
        return tuple(self.factors)

    def get_next_prime_factor(self, n):
        if n % 2 == 0:
            return 2
        for x in range(3, int(math.ceil(math.sqrt(n)) + 1), 2):
            if n % x == 0:
                return x
        return int(n)


