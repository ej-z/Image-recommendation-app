class Img_Img_Data:

    def print_graph(self, ids, graph, k):
        file = open("img_img_graph.txt", "w")
        for index, g in enumerate(graph):
            image_id = ids[index]
            file.write(str(image_id) + " = {")
            for img in g:
                id = ids[img['id']]
                dist = img['dist']
                file.write(str(id) + " : " + str(dist) + "; ")
            file.write(" }\n")
            # if index > 0:
            #     break
        file.close()
        print("Graph written to file  - img_img_graph.txt. Please open to see the graph")

    def __init__(self,ids, g, k):
        self.img_ids = ids
        self.graph = g
        self.k = k

        self.print_graph(ids, g, k)