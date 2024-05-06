import requests
import datetime
import re
import os
from typing import Optional
from urllib.parse import urljoin
from bs4 import BeautifulSoup, element
import pandas as pd
from bill import Bill
from cloud_storage_client import CloudStorageClient
from date_util import DateUtil


class Crawler:
    SOURCE_URL = "https://www.shugiin.go.jp/internet/itdb_gian.nsf/html/gian/"
    BILL_URL_SUFFIX = "kaiji{}.htm"
    DATETIME_PATTERN = r'^(\D+)(\d+)年(\d+)月(\d+)日$'
    OUTPUT_DIR = "./output"

    def __init__(self, diet_no: int) -> None:
        self.__diet_no = diet_no
        self.__source_url = urljoin(
            Crawler.SOURCE_URL,
            Crawler.BILL_URL_SUFFIX.format(diet_no)
        )
        self.__output_file_name = "bill_of_row_diet{}.csv".format(self.__diet_no)
        self.__output_file_path = Crawler.OUTPUT_DIR + self.__output_file_name 

        print("対象URL: {}".format(self.__source_url))

    def run(self) -> None:
        print("第{}回国会の議案情報のクローリングを開始します。".format(self.__diet_no))
        response = requests.get(self.__source_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        low_tables = soup.find_all("table")
        bills = []
        for table in low_tables:
            caption = table.find("caption").text
            if caption == "衆法の一覧":
                bills += self.retrieve_bills(table, "衆法")
            elif caption == "参法の一覧":
                bills += self.retrieve_bills(table, "参法")
            elif caption == "閣法の一覧":
                bills += self.retrieve_bills(table, "閣法")
        print("クローリングが完了しました。")
        self.export_to_csv(bills)

    def retrieve_bills(self, table: element.ResultSet, bill_type: str) -> list[dict]:
        print("{}のクローリングを実施します。".format(bill_type))
        bills = []

        trs = table.find_all("tr")
        # 1行目はヘッダー。期待通りの列順でなければエラー。
        header_tr = trs[0]
        header = [td.text for td in header_tr.find_all("th")]
        assert (header == ['提出回次', '番号', '議案件名', '審議状況', '経過情報', '本文情報'])

        # 表からデータを取得
        for tr in trs[1:]:
            low_dict = {}
            low_dict["diet_no"] = self.__diet_no
            low_dict["bill_type"] = bill_type
            tds = tr.find_all("td")
            low_dict["submit_diet_no"] = tds[0].text
            low_dict["submit_bill_no"] = tds[1].text
            low_dict["bill_subject"] = tds[2].text
            low_dict["status"] = tds[3].text
            progress_href = tds[4].find("a").get("href")
            progress_dict = self.retrieve_progress(
                urljoin(Crawler.SOURCE_URL, progress_href)
            )
            body_href = tds[5].find("a").get("href") \
                if tds[5].find("a") \
                else None
            low_dict["body_link"] = urljoin(Crawler.SOURCE_URL, body_href)
            low_dict.update(progress_dict)
            bill = Bill.from_dict(low_dict)
            bills.append(bill)
        return bills

    def retrieve_progress(self, url: str) -> dict:
        progress_dict = {}
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all("table")
        keika_table = tables[0]
        for tr in keika_table.find_all("tr")[1:]:
            tds = tr.find_all("td")
            name = tds[0].text
            contents = tds[1].text.strip()
            if name == "議案提出者":
                progress_dict["submit_person"] = contents
            elif name == "議案提出会派":
                progress_dict["submit_parties"] = contents
            elif name == "衆議院議案受理年月日":
                progress_dict["representatives_accept_date"] = self.transform_datetime(
                    contents)
            elif name == "衆議院審議終了年月日／衆議院審議結果":
                progress_dict["representatives_finish_date"] = self.transform_datetime(
                    contents.split("／")[0])
                if len(contents) > 1:
                    progress_dict["representatives_deliveration_result"] = \
                        contents.split("／")[1].strip()
            elif name == "参議院議案受理年月日":
                progress_dict["councilors_accept_date"] = \
                    self.transform_datetime(contents)
            elif name == "参議院審議終了年月日／参議院審議結果":
                progress_dict["councilors_finish_date"] = \
                    self.transform_datetime(contents.split("／")[0])
                if len(contents) > 1:
                    progress_dict["councilors_deliveration_result"] = \
                        contents.split("／")[1].strip()
            elif name == "公布年月日／法律番号":
                progress_dict["promulgation_date"] = \
                    self.transform_datetime(contents.split("／")[0])
        return progress_dict

    # 日時変換(「令和 6年 1月26日」 -> 2024/1/26)
    def transform_datetime(self, datetime_str: str) -> Optional[datetime.datetime]:
        if not datetime_str:
            return None
        clean_datetime_str = datetime_str.strip().replace(" ", "")
        wareki, year, month, day = re.findall(
            Crawler.DATETIME_PATTERN, clean_datetime_str
        )[0]
        return DateUtil.transform_to_western_year(wareki, int(year), int(month), int(day))

    def export_to_csv(self, bills: list) -> None:
        df = pd.DataFrame(bills)

        csv = df.to_csv(
            index_label="bill_id",
            quoting=1,
            escapechar="\\"
        )

        CloudStorageClient().upload_csv(csv, self.__output_file_name)
        print("GCSへのアップロードが完了しました。")
