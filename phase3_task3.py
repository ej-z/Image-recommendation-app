from page_rank_algorithms import PageRanks

class Phase3_task3:

    def task_3(self, data, k):

        pr = PageRanks()
        ranks = pr.page_rank(data)
        print(ranks.nlargest(k))