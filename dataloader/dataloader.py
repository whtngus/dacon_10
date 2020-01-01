import json
import os
from PIL import Image

class DataLoader():
    def __init__(self,data_path):
        self.data_path = self._data_path_set(data_path)


    def _data_path_set(self,data_path):
        '''
            데이터 경로 매칭
        :param data_path:
        :return:
        '''
        data_path_map = {}
        for directorys in os.listdir(data_path):
            target_path = os.path.join(data_path + "/" +directorys)
            for data_name in os.listdir(target_path):
                file_path = os.path.join(target_path + "/" + data_name)
                data_path_map[data_name] = file_path
        return data_path_map

    def data_load(self,label_path,write_path):
        '''
        사진의 배부분과 결과를 따로잘라서 추출
        - 사진
        - 라벨및 추가 데이터
        인덱스  파일명  위경도 사이즈  라벨
        위경도 사이즈 : (위도 사이즈 차 * 10,000) * (경도 사이즈 차 * 10,000)
        :param label_path:
        :param write_path:
        :return:
        '''
        text_f = open(write_path + "/write.txt","w",encoding="utf-8")
        text_f.write("index\tfile_name\tdata size\tlabel\n")
        line_count = 0
        json_datas = ""
        with open(label_path,"r",encoding="utf-8") as json_file:
            json_datas = json.load(json_file)
        for json_data in json_datas["features"]:
            image_name = json_data["properties"]["image_id"]
            type_id = json_data["properties"]["type_id"]
            img = Image.open(self.data_path[image_name])
            data_range = json_data["geometry"]["coordinates"][0]
            target_size = abs((data_range[0][0] - data_range[2][0]) * 10000) * abs((data_range[0][1] - data_range[2][1]) * 10000)
            image_range = json_data["properties"]["bounds_imcoords"].split(",")
            crop_img = img.crop(image_range)
            write_file_name = str(line_count) + ".png"
            crop_img.save(write_path + "/" + write_file_name)
            text_f.write(str(line_count) + "\t" + write_file_name + +"\t" + str(target_size) + "\t" + str(type_id) +"\n")
            line_count += 1


if __name__ == "__main__":
    label_path = "../data/labels.json"
    data_path = "../data/train"
    write_path = "../data/train_embedding"
    data_loader = DataLoader(data_path)
    data_loader.data_load(label_path,write_path)