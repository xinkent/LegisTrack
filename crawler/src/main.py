from dotenv import find_dotenv, load_dotenv
from crawler import Crawler
import argparse

def execute(request) -> None:
   diet_no = 213
   Crawler(diet_no).run() 
   return "OK"

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    parser = argparse.ArgumentParser()
    parser.add_argument("--diet_no", help="対象国会回次", type=int, default=213,)
    parser.add_argument("--output_dir", help="出力先ディレクトリ",
                        type=str, default="./outputs/")
    args = parser.parse_args()
    diet_no = args.diet_no
    Crawler(diet_no).run()
