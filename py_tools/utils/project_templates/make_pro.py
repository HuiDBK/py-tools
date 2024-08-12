#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: Hui
# @File: project_template.py
# @Desc: { 项目模板工具模块 }
# @Date: 2024/04/26 17:46
import argparse
import os
import shutil
from pathlib import Path

from loguru import logger

# 项目基准目录
BASE_DIR = Path(__file__).parent.parent.parent.parent

template_dir = os.path.dirname(__file__)
py_template_dir = os.path.join(template_dir, "python_project")


def gen_py_project(project_name):
    logger.info(f"Generating Python project [{project_name}] structure...")

    # 创建项目目录
    os.makedirs(project_name, exist_ok=True)

    # 创建 README.md 文件
    with open(os.path.join(project_name, "README.md"), "w") as readme:
        readme.write("# Project: " + project_name)

    # 创建 main.py 文件（示例中简单创建一个空文件）
    with open(os.path.join(project_name, "main.py"), "w") as main_file:
        main_file.write("# 主入口模块")

    # 创建 requirements.txt 文件（示例中简单创建一个空文件）
    with open(os.path.join(project_name, "requirements.txt"), "w") as requirements:
        requirements.write("hui-tools")

    # 创建 pre-commit-config.yaml、ruff.toml 文件
    shutil.copy(src=BASE_DIR / ".pre-commit-config.yaml", dst=os.path.join(project_name, ".pre-commit-config.yaml"))
    shutil.copy(src=BASE_DIR / "ruff.toml", dst=os.path.join(project_name, "ruff.toml"))

    # 创建 docs 目录
    os.makedirs(os.path.join(project_name, "docs"), exist_ok=True)

    # 创建 src 目录及其子目录
    target_dir = os.path.join(project_name, "src")
    src_dir = os.path.join(py_template_dir, "src")
    shutil.copytree(src_dir, target_dir, dirs_exist_ok=True)

    # 创建 tests 目录
    os.makedirs(os.path.join(project_name, "tests"), exist_ok=True)

    logger.info(f"Python project [{project_name}] generated successfully.")


def make_project_python(args):
    project_name = args.project_name
    try:
        gen_py_project(project_name)
    except Exception:
        logger.exception("Failed to generate Python project.")
        shutil.rmtree(project_name, ignore_errors=True)


def make_project_java(args):
    print(f"Generating Java project [{args.project_name}] structure...")
    # Add code to generate Java project structure


def make_project():
    parser = argparse.ArgumentParser(description="Generate project structure.")
    subparsers = parser.add_subparsers(dest="subcommand")

    project_parser = subparsers.add_parser("make_project")
    project_parser.add_argument("project_name", help="Name of the project")
    project_parser.add_argument("--python", action="store_true", help="Generate Python project structure")
    project_parser.add_argument("--java", action="store_true", help="Generate Java project structure")

    args = parser.parse_args()

    if args.subcommand == "make_project":
        if args.python:
            make_project_python(args)
        elif args.java:
            make_project_java(args)
        else:
            make_project_python(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    make_project()
