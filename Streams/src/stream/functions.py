from stream import Stream
null_stream = (None, None)

class MapStream(Stream):
    def __init__(self, fn, stream):
        super(MapStream, self).__init__()
        self.fn = fn
        self.stream = stream

    def popNext(self):
        val = self.stream.popNext()
        return self.fn(val)

    def popN(self,num_N):
        n_poped_list = []
        while num_N:
            n_poped_list.append(self.popNext())
            num_N -= 1
        return n_poped_list

class FilterStream(Stream):
    def __init__(self, pred, stream):
        super(FilterStream, self).__init__()
        self.pred = pred
        self.stream = stream

    def popNext(self):
        val = None
        while True:
            val = self.stream.popNext()
            if self.pred(val):
                break
        return val

    def popN(self,num_N):
        n_poped_list = []
        while num_N:
            n_poped_list.add(self.popNext())
            num_N -= 1
        return n_poped_list

class ZipWithStream(Stream):
    def __init__(self, fn, streamA, streamB):
        super(ZipWithStream, self).__init__()
        self.fn = fn
        self.streamA = streamA
        self.streamB = streamB

    def popNext(self):
        valA = self.streamA.popNext()
        valB = self.streamB.popNext()

        if valA is None or valB is None:
            return None
        return self.fn(valA, valB)

    def popN(self,num_N):
        n_poped_list = []
        while num_N:
            n_poped_list.append(self.popNext())
            num_N -= 1
        return n_poped_list

class PrefixReduceStream(Stream):
    def __init__(self, fn, stream, init):
        super(PrefixReduceStream, self).__init__()
        self.fn = fn
        self.stream = stream
        self.init = init
        self.currentval = init

    def popNext(self):
        self.currentval = self.fn(self.currentval, self.stream.popNext())
        return self.currentval


    def popN(self,num_N):
        n_poped_list = []
        while num_N:
            n_poped_list.append(self.popNext())
            num_N -= 1
        return n_poped_list

def map(fn, stream):
    if stream is null_stream: return null_stream
    return MapStream(fn, stream)

def filter(pred, stream):
    if stream is null_stream: return null_stream
    return FilterStream(pred, stream)

def zipWith(fn, streamA, streamB):
    if streamA is null_stream or streamB is null_stream:
        return null_stream
    return ZipWithStream(fn, streamA, streamB)

def prefixReduce(fn, stream, init):
    if stream is null_stream: return init
    return PrefixReduceStream(fn, stream, init)

def head((H, _)):
    return H

def tail((_, T)):
    return T()


