# main.py

import os  
import pandas as pd  
from rich.progress import track  
from get_main_body import get_all_main_body  
from get_comments_level_one import get_all_level_one  
from get_comments_level_two import get_all_level_two  
import logging  
  
logging.basicConfig(level=logging.INFO)  
  
  
class WBParser:  
    def __init__(self, cookie):  
        self.cookie = cookie  
  
        os.makedirs("./WBData", exist_ok=True)  
        os.makedirs("./WBData/Comments_level_1", exist_ok=True)  
        os.makedirs("./WBData/Comments_level_2", exist_ok=True)  
        self.main_body_filepath = "./WBData/demo.csv"  
        self.comments_level_1_filename = "./WBData/demo_comments_one.csv"  
        self.comments_level_2_filename = "./WBData/demo_comments_two.csv"  
        self.comments_level_1_dirpath = "./WBData/Comments_level_1/"  
        self.comments_level_2_dirpath = "./WBData/Comments_level_2/"  
  
    def get_main_body(self, q, kind):  
        data = get_all_main_body(q, kind, self.cookie)  
        data = data.reset_index(drop=True).astype(str).drop_duplicates()  
        data.to_csv(self.main_body_filepath, encoding="utf_8_sig")  
  
    def get_comments_level_one(self):  
        data_list = []  
        main_body = pd.read_csv(self.main_body_filepath, index_col=0)  
  
        logging.info(f"主体内容一共有{main_body.shape[0]:5d}个，现在开始解析...")  
  
        for ix in track(range(main_body.shape[0]), description=f"解析中..."):  
            uid = main_body.iloc[ix]["uid"]  
            mid = main_body.iloc[ix]["mid"]  
            final_file_path = f"{self.comments_level_1_dirpath}{uid}_{mid}.csv"  
  
            if os.path.exists(final_file_path):  
                length = pd.read_csv(final_file_path).shape[0]  
                if length > 0:  
                    continue  
  
            data = get_all_level_one(uid=uid, mid=mid, cookie=self.cookie)  
            data.drop_duplicates(inplace=True)  
            data.to_csv(final_file_path, encoding="utf_8_sig")  
            data_list.append(data)  
        logging.info(f"主体内容一共有{main_body.shape[0]:5d}个，已经解析完毕！")  
        data = pd.concat(data_list).reset_index(drop=True).astype(str).drop_duplicates()  
        data.to_csv(self.comments_level_1_filename)  
  
    def get_comments_level_two(self):  
        data_list = []  
        comments_level_1_data = pd.read_csv(self.comments_level_1_filename, index_col=0)  
  
        logging.info(  
            f"一级评论一共有{comments_level_1_data.shape[0]:5d}个，现在开始解析..."  
        )  
  
        for ix in track(  
            range(comments_level_1_data.shape[0]), description=f"解析中..."  
        ):  
            main_body_uid = comments_level_1_data.iloc[ix]["main_body_uid"]  
            mid = comments_level_1_data.iloc[ix]["mid"]  
            final_file_path = (  
                f"{self.comments_level_2_dirpath}{main_body_uid}_{mid}.csv"  
            )  
  
            if os.path.exists(final_file_path):  
                length = pd.read_csv(final_file_path).shape[0]  
                if length > 0:  
                    continue  
  
            data = get_all_level_two(uid=main_body_uid, mid=mid, cookie=self.cookie)  
            data.drop_duplicates(inplace=True)  
            data.to_csv(final_file_path, encoding="utf_8_sig")  
            data_list.append(data)  
        logging.info(  
            f"一级评论一共有{comments_level_1_data.shape[0]:5d}个，已经解析完毕！"  
        )  
        data = pd.concat(data_list).reset_index(drop=True).astype(str).drop_duplicates()  
        data.to_csv(self.comments_level_2_filename)  
  
  
if __name__ == "__main__":  
    q = "#上海租房#"  # 话题  
    kind = "综合"  # 综合，实时，热门，高级  
    cookie = "UOR=,,link.csdn.net; SCF=Aom2bqRNBWocgmFcqGgvNobxM89SxENXXSokReRACKPu3lnnfEhZ1oU_Vziie2ASlVSL9-gbdGq-LDZIQumdg6E.; SINAGLOBAL=3147833289802.149.1743398950990; SUB=_2A25FS8LvDeRhGeFH4lAQ9CfFyzuIHXVmKVonrDV8PUNbmtANLUT7kW9Neh_I4Gm2XwtpjW-L87MGb9AxqdE2QpF8; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhJSwgJ-DlwKEw-1L.2VsU45JpX5KzhUgL.FoM41KzpSh.4ehM2dJLoIpeLxKnLB.BLBoqLxKqLBK5LBoM_; ALF=02_1752645567; _s_tentry=passport.weibo.com; Apache=9705319955700.31.1750053570344; ULV=1750053570379:12:1:1:9705319955700.31.1750053570344:1743398950993"  # 设置你的cookie
    wbparser = WBParser(cookie)  
    wbparser.get_main_body(q, kind) # 获取主体内容  
    wbparser.get_comments_level_one() # 获取一级评论
    wbparser.get_comments_level_two() # 获取二级评论
