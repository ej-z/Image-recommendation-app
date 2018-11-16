from page_rank_algorithms import PageRanks
from UI.PicturesApp import PicturesApp

class Phase3_task3:

    def task_3(self, data, k):

        pr = PageRanks()
        ranks = pr.page_rank(data)

        result = ranks.nlargest(k)

        pic_info = []

        for idx, val in result.iteritems():
            pic_info.append({'id': idx, 'info': idx + ' :'+str(val)})

        PicturesApp(pic_info).run()
