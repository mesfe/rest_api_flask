# import json
# import models
#
#
#
#
# def main():
#
# j=json.load(open("../avian_sempra_11_2.dataset.json","r"))
#
#
#
#
# datasetobject= models.Dataset.from_json(j)
# datasetobject.save()
# for x in j.get("data"):
#     imageobject=models.Image.from_json(x, datasetobject)
#     imageobject.save()
#     for y in x.get("annotationHistory",imageobject):
#         annotationobject = models.AnnotationSession.from_json(y, imageobject)
#         annotationobject.save()
#         for z in y.get("clusters",annotationobject):
#             clusterobject = models.Cluster.from_json(z, annotationobject)
#             clusterobject.save()
#
#
# # if __name__ == '__main__':
# #     main()
#
