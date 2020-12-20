import os

from ImageSimilarity import ImageSimilarity
from ReportFoto import ReportFoto


class ImageWorker:

    def generate_reportfoto(self):
        lista_foto_scaricate = self.get_path_files("photo_downloaded\\")
        correttezza_logo = self.find_and_classify_logo(lista_foto_scaricate)
        presenza_competitors = self.find_competitors(lista_foto_scaricate)
        presenza_scritte_foto = self.find_keywords_in_images(lista_foto_scaricate)
        report_foto = ReportFoto(correttezza_logo, presenza_competitors, presenza_scritte_foto)
        return report_foto

    def find_and_classify_logo(self, lista_foto_scaricate):
        img_ssim = ImageSimilarity()
        lista_foto_competitors = self.get_path_files("dataset_image_ssim\\competitors\\")
        lista_foto_creo_errati = self.get_path_files("dataset_image_ssim\\creo ERRATI\\")
        lista_foto_creo_ni = self.get_path_files(
            "dataset_image_ssim\\creo loghi ok ma proporzioni o abbinamenti NON CORRETTI\\")
        lista_foto_creo_ok = self.get_path_files("dataset_image_ssim\\creo TUTTO OK\\")
        lista_foto_lubecreo_errati = self.get_path_files("dataset_image_ssim\\lube&creo ERRATI\\")
        lista_foto_lubecreo_ni = self.get_path_files(
            "dataset_image_ssim\\lube&creo loghi ok ma proporzioni o abbinamenti NON CORRETTI\\")
        lista_foto_lubecreo_ok = self.get_path_files("dataset_image_ssim\\lube&creo TUTTO OK\\")
        lista_foto_lube_ni = self.get_path_files(
            "dataset_image_ssim\\lube loghi ok ma proporzioni o abbinamenti NON CORRETTI\\")
        lista_foto_lube_ok = self.get_path_files("dataset_image_ssim\\lubeTUTTO OK\\")
        lista_foto_lube_errati = self.get_path_files("dataset_image_ssim\\lubeERRATI\\")
        lista_foto_notlogo = self.get_path_files("dataset_image_ssim\\NOT LOGO\\")
        # TODO : for che scorre le foto
        Dict = {}
        for x in lista_foto_scaricate:
            result = [0] * 11
            for l1 in lista_foto_competitors:
                tmp1 = img_ssim.compare(x, l1)
                result[0] = tmp1 if tmp1 > result[0] else result[0]
            for l2 in lista_foto_creo_errati:
                tmp2 = img_ssim.compare(x, l2)
                result[1] = tmp2 if tmp2 > result[1] else result[1]
            for l3 in lista_foto_creo_ni:
                tmp3 = img_ssim.compare(x, l3)
                result[2] = tmp3 if tmp3 > result[2] else result[2]
            for l4 in lista_foto_creo_ok:
                tmp4 = img_ssim.compare(x, l4)
                result[3] = tmp4 if tmp4 > result[3] else result[3]
            for l5 in lista_foto_lubecreo_errati:
                tmp5 = img_ssim.compare(x, l5)
                result[4] = tmp5 if tmp5 > result[4] else result[4]
            for l6 in lista_foto_lubecreo_ni:
                tmp6 = img_ssim.compare(x, l6)
                result[5] = tmp6 if tmp6 > result[5] else result[5]
            for l7 in lista_foto_lubecreo_ok:
                tmp7 = img_ssim.compare(x, l7)
                result[6] = tmp7 if tmp7 > result[6] else result[6]
            for l8 in lista_foto_lube_ni:
                tmp8 = img_ssim.compare(x, l8)
                result[7] = tmp8 if tmp8 > result[7] else result[7]
            for l9 in lista_foto_lube_ok:
                tmp9 = img_ssim.compare(x, l9)
                result[8] = tmp9 if tmp9 > result[8] else result[8]
            for l10 in lista_foto_lube_errati:
                tmp10 = img_ssim.compare(x, l10)
                result[9] = tmp10 if tmp10 > result[9] else result[9]
            for l11 in lista_foto_notlogo:
                print("---->" + x)
                tmp11 = img_ssim.compare(x, l11)
                print(tmp11)
                result[10] = tmp11 if tmp11 > result[10] else result[10]

            print(result)
            index_result_max = result.index(max(result))
            options = {0: " competitors",
                       1: " creo errati",
                       2: " creo ni",
                       3: " creo ok",
                       4: " lube e creo errati",
                       5: " lube e creo ni",
                       6: " lube e creo ok",
                       7: " lube ni",
                       8: " lube ok",
                       9: " lube errati",
                       10: " not logo"
                       }
            print(x + options.get(index_result_max) + " percentuale : " + str(result[index_result_max]))

            # risultato =
            # result.append()
            # print(str(result))
            # Dict["competitors"] = result
            # result.clear()

        # TODO: step1 image similarity su una fot

    def find_competitors(self, lista_foto_scaricate):
        pass

    def find_keywords_in_images(self, lista_foto_scaricate):
        pass

    def get_path_files(self, path):
        # mypath = "photo_downloaded\\"
        mypath2 = "C:\\Users\\matti\\git\\ProgettoLube\\ProgettoLube\\WebInspector\\"
        paths = [os.path.join(path, fn) for fn in next(os.walk(path))[2]]
        temp = []
        for x in paths:
            temp.append(mypath2 + x)
        return temp



