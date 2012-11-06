import stream
import stream.functions

# ---------
# Question!
# Why use a static list instead of a function in a unit test verifying
# the prime stream.
PRIME_STREAM = (2,3,5,7,11,13,17,19,23,29,
                31,37,41,43,47,53,59,61,67,71,
                73,79,83,89,97,101,103,107,109,113,
                127,131,137,139,149,151,157,163,167,173,
                179,181,191,193,197,199,211,223,227,229,
                233,239,241,251,257,263,269,271,277,281,
                283,293,307,311,313,317,331,337,347,349,
                353,359,367,373,379,383,389,397,401,409,
                419,421,431,433,439,443,449,457,461,463,
                467,479,487,491,499,503,509,521,523,541,
                547,557,563,569,571,577,587,593,599,601,
                607,613,617,619,631,641,643,647,653,659,
                661,673,677,683,691,701,709,719,727,733,
                739,743,751,757,761,769,773,787,797,809,
                811,821,823,827,829,839,853,857,859,863,
                877,881,883)

PRIME_FACTOR_STREAM_CASES = ({
                                 "input" : 1,
                                 "values" : []
                             },{
                                 "input" : 10,
                                 "values" : [2,5]
                             },{
                                 "input" : 20,
                                 "values" : [2,5]
                             },{
                                 "input" : 25,
                                 "values" : [5]
                             },{
                                 "input" : 1155,
                                 "values" : [3, 5, 7, 11]
                             })

HIGH_ORDER_STREAM_CASES = ({
                               "inputStream" : stream.functions.map(lambda x: x * 2, stream.Primes()),
                               "expected" : [p * 2 for p in PRIME_STREAM],
                               "isFinite" : False
                           },{
                               "inputStream" : stream.functions.filter(lambda x: (x+1) % 3 == 0, stream.Primes()),
                               "expected" : [p for p in PRIME_STREAM if (p+1) % 3 == 0],
                               "isFinite" : False
                           },{
                               "inputStream" : stream.functions.filter(lambda x: x < 10 or x > 100, stream.Primes()),
                               "expected" : [p for p in PRIME_STREAM if p < 10 or p > 100],
                               "isFinite" : False
                           },{
                               "inputStream" : stream.functions.zipWith(lambda a,b: (a,b), stream.Primes(), stream.PrimeFactors(1155)),
                               "expected" : [(2, 3), (3, 5), (5, 7), (7, 11)],
                               "isFinite" : True
                           },{
                               "inputStream" : stream.functions.prefixReduce(lambda x,y: x+y, stream.Primes(), 0),
                               "expected" : [2, 5, 10, 17, 28, 41, 58, 77, 100, 129,
                                             160, 197, 238, 281, 328, 381, 440, 501,
                                             568, 639, 712, 791, 874, 963, 1060, 1161,
                                             1264, 1371, 1480, 1593, 1720, 1851, 1988,
                                             2127, 2276, 2427, 2584, 2747, 2914, 3087,
                                             3266, 3447, 3638, 3831, 4028, 4227, 4438,
                                             4661, 4888, 5117, 5350, 5589, 5830, 6081,
                                             6338, 6601, 6870, 7141, 7418, 7699, 7982,
                                             8275, 8582, 8893, 9206, 9523, 9854, 10191,
                                             10538, 10887, 11240, 11599, 11966, 12339],
                               "isFinite" : False
                           }
                           ,{
                               "inputStream" :
                                   stream.functions.filter(lambda x: x % 3 == 0,
                                       stream.functions.map(lambda x: x + 1,
                                           stream.Primes())),

                               "expected" : [x for x in [p + 1 for p in PRIME_STREAM] if x % 3 == 0],
                               "isFinite" : False
                           }
    )

def test_randomStream():
    randomStream = stream.Randoms()

    previousNumbers = set()
    for __ in xrange(1000):
        next = randomStream.popNext()
        assert next not in previousNumbers
        assert isinstance(next, int)
        previousNumbers.add(next)

def test_primeStream_Values():
    primeStream = stream.Primes()
    for prime in PRIME_STREAM:
        next = primeStream.popNext()
        assert prime == next

def test_primeStream_2000():
    primeStream = stream.Primes()

    for _ in xrange(2000):
        assert primeStream.popNext() is not None

def test_primeFactorStream(input, values):
    primeFactorStream = stream.PrimeFactors(input)

    primes = []

    while True:
        next = primeFactorStream.popNext()
        if next is None:
            break

        primes.append(next)

    # Verify all of the prime factors are there.
    for prime in values:
        assert prime in primes

    # Verify the prime factors are returned only once
    assert len(values) == len(primes)

def test_highOrderStreams(inputStream, expected, isFinite):
    for expNext in expected:
        actNext = inputStream.popNext()
        assert expNext == actNext

    if isFinite:
        assert inputStream.popNext() is None
        assert inputStream.popNext() is None

# ---------
# Question!
# Finish this test case for popN reusing HIGH_ORDER_STREAM_CASES
def test_popN(inputStream, expected, isFinite):
    if isFinite:
        for exp in expected:
            result_list = inputStream.popN(len(exp))
            assert len(exp) == len(result_list)
    return True

def pytest_generate_tests(metafunc):
    if metafunc.function.__name__ == test_primeFactorStream.__name__:
        map(lambda tc: metafunc.addcall(funcargs=tc), PRIME_FACTOR_STREAM_CASES)

    if metafunc.function.__name__ in (test_highOrderStreams.__name__,
                                      test_popN.__name__):
        map(lambda tc: metafunc.addcall(funcargs=tc), HIGH_ORDER_STREAM_CASES)
