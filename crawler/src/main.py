from crawler import Crawler
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--diet_no", help="対象国会回次", type=int, default=213,)
    parser.add_argument("--output_dir", help="出力先ディレクトリ",
                        type=str, default="./outputs/")
    args = parser.parse_args()
    diet_no = args.diet_no
    Crawler(diet_no).run()
