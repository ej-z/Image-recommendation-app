from page_rank_algorithms import PageRanks
import UI.HTMLPicGallery as PA

class Phase3_task4:

    def task_4(self, data, k):

        pr = PageRanks()
        # ranks = pr.personalized_page_rank(data,['2976144', '3172496917', '2614355710'])

        ranks = pr.personalized_page_rank(data, ['872138825', '3172496917', '2614355710'])
        result = ranks.nlargest(k)

        pic_info = []

        for idx, val in result.iteritems():
            pic_info.append({'id': idx, 'info': idx + ' :'+str(val)})

        PA.display_images(pic_info)
        PA.display_images([{'id': '872138825', 'info': '1'}, {'id': '3172496917', 'info': '1'}, {'id': '2614355710', 'info': '1'}])
