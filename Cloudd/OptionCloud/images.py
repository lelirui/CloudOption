import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), 'util'))

from util import xmltodict
import re


class instanceImage():
    def __init__(self,client):
        self.client=client

    def parse_images(self,images, image_name):
        try:
            v = images['DescribeImagesResponse']['imagesSet']['item']
            if type(v).__name__ == 'list':
                for item in v:
                    if item["imageState"] == "available" and item["imageState"] == "available" and item[
                        "name"] == image_name:
                        return item["imageId"]
                return None
            elif type(v).__name__ == 'OrderedDict':
                if v["imageState"] == "available" and v["imageState"] == "available" and v["name"] == image_name:
                    return v["imageId"]
                return None
        except Exception as e:
            return None

    def JudgeIsExistImage(self,images,imageId):
        try:
            v = images['DescribeImagesResponse']['imagesSet']['item']
            if type(v).__name__ == 'list':
                for item in v:
                    if item["imageState"] == "available" and item["imageState"] == "available" and item[
                        "imageId"] == imageId:
                        return item["imageId"]
                return None
            elif type(v).__name__ == 'OrderedDict':
                if v["imageState"] == "available" and v["imageState"] == "available" and v["imageId"] == imageId:
                    return v["imageId"]
                return None
        except Exception as e:
            return None


    def DudgeImages(self):
        # params = {"Filter.1.Name": "imageId", "Filter.1.Value.1": imageId}
        result = self.client.invoke("DescribeImages", {})
        return xmltodict.parse(result, encoding='utf-8')

    def get_image_id(self,image):
        if re.match('ami',image):
            image_id = self.JudgeIsExistImage(self.DudgeImages(),image)
        else:
            image_id = self.parse_images(self.DudgeImages(), image)
        if not image_id:
            return 'not'
        return image_id

    def import_s3_image(self,s3url, architecture, platform, storageId, shared, imageName, bootloader='mbr'):
        params = {"Url": s3url, "Architecture": architecture, "Platform": platform, "StorageId": storageId,
                  "Shared": shared, "Bootloader": bootloader, "ImageName": imageName}
        importresult= self.client.invoke("ImportImage", params)
   #     print(importresult)
        try:
            importresultXML=xmltodict.parse(importresult, encoding='utf-8')
            return importresultXML["ImportImageResponse"]["imageId"]
        except Exception as e:
            return None

    def REstelIMage(self,image_id, architecture, platform, storageId, shared, imageName, bootloader='mbr'):
        params = {"ImageId": image_id,"Attribute":'description'}
        importresult = self.client.invoke("ModifyImageAttribute", params)
   #     print(importresult)
        try:
            importresultXML = xmltodict.parse(importresult, encoding='utf-8')
            # return importresultXML["ImportImageResponse"]["imageId"]
        except Exception as e:
            return None

    def RegisterImage(self):
        params={"ImageLocation":'common-ami-E92EA3B0.images.manifest.xml'}
   #     print(self.client.invoke("RegisterImage",params))


# client=cloudutil.bcclient()
# image=instanceImage(client)
# print(image.get_image_id('ami-BC00FF12'))