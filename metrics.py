import numpy as np

class Metrics():

    def precision_at_k(self, r, k):
        assert k >= 1
        r = np.asarray(r)[:k] != 0
        if r.size != k:
            raise ValueError('Relevance score length < k')
        return np.mean(r)

    def average_precision(self, r):
        r = np.asarray(r) != 0
        out = [self.precision_at_k(r, k + 1) for k in range(r.size) if r[k]]
        if not out:
            return 0.
        return np.mean(out)

    def mean_average_precision(self, rs):
        return np.mean([self.average_precision(r) for r in rs])

    def dcg_at_k(self, r, k):
        r = np.asfarray(r)[:k]
        if r.size:
            return np.sum(np.subtract(np.power(2, r), 1) / np.log2(np.arange(2, r.size + 2)))
        return 0.


    def ndcg_at_k(self, r, k):
        idcg = self.dcg_at_k(sorted(r, reverse=True), k)
        if not idcg:
            return 0.
        return self.dcg_at_k(r, k) / idcg
