#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# @Time    : 2025/8/13 上午8:37
# @Author  : 单子叶蚕豆_DzyCd
# @File    : run.py
# @IDE     : PyCharm
from main_wh import run

import argparse


def main():
    parser = argparse.ArgumentParser(description="Run the model with specified parameters.")

    parser.add_argument("--OPENAI_API_KEY", required=True, type=str, help="openai api key")
    parser.add_argument("--model", type=str, default="gpt-4o-mini",
                        help="The model to use.")
    parser.add_argument("--temperature", type=float, default=0.2,
                        help="The temperature setting for the model.")
    parser.add_argument("--request_timeout", type=int, default=60,
                        help="The request timeout in seconds.")
    parser.add_argument("--base_url", type=str, default="https://cn2us02.opapi.win/v1",
                        help="The base URL for the API.")
    parser.add_argument("--target_repo_path", type=str, default=r"E:\Pycharm_projects\nonebot-plugin-ImageLibrary",
                        help="The path to the target repository.")
    parser.add_argument("--hierarchy_path", type=str, default=".project_doc_record",
                        help="The path to the hierarchy record.")
    parser.add_argument("--markdown_docs_path", type=str, default="markdown_docs",
                        help="The path to the markdown documents.")
    parser.add_argument("--ignore_list", type=str, default="",
                        help="A comma-separated list of items to ignore.")
    parser.add_argument("--language", type=str, default="English",
                        help="The language for the documentation.")
    parser.add_argument("--max_thread_count", type=int, default=4,
                        help="The maximum number of threads to use.")
    parser.add_argument("--log_level", type=str, default="INFO",
                        help="The logging level.")
    parser.add_argument("--print_hierarchy", action="store_true",
                        help="Whether to print the hierarchy. Default is False.")

    args = parser.parse_args()

    args_dict = vars(args)

    run(**args_dict)


if __name__ == "__main__":
    main()
