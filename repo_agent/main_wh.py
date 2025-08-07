import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(".."))
from importlib import metadata

import click
from pydantic import ValidationError

from repo_agent.doc_meta_info import DocItem, MetaInfo
from repo_agent.log import logger, set_logger_level_from_config
from repo_agent.runner import Runner, delete_fake_files
from repo_agent.settings import SettingsManager, LogLevel
from repo_agent.utils.meta_info_utils import delete_fake_files, make_fake_files

try:
    version_number = metadata.version("repoagent")
except metadata.PackageNotFoundError:
    version_number = "0.0.0"


def handle_setting_error(e: ValidationError):
    """处理设置的配置错误。"""
    # 输出更详细的字段缺失信息，使用颜色区分
    for error in e.errors():
        field = error["loc"][-1]
        if error["type"] == "missing":
            message = click.style(
                f"缺少必需字段 `{field}`。请设置 `{field}` 环境变量。",
                fg="yellow",
            )
        else:
            message = click.style(error["msg"], fg="yellow")
        click.echo(message, err=True, color=True)

    # 使用 ClickException 优雅地退出程序
    raise click.ClickException(
        click.style(
            "由于配置错误，程序终止。", fg="red", bold=True
        )
    )


def run(
    model="gpt-4o-mini",
    temperature=0.2,
    request_timeout=60,
    base_url="https://aigptx.top/v1",
    target_repo_path="/home/david/WH/projects/simdjson",
    hierarchy_path=".project_doc_record",
    markdown_docs_path="markdown_docs",
    ignore_list="",
    language="English",
    max_thread_count=4,
    log_level="INFO",
    print_hierarchy=False,
):
    """运行程序并指定参数。"""
    try:
        # 使用 SettingsManager 获取并验证设置
        setting = SettingsManager.initialize_with_params(
            target_repo=target_repo_path,
            hierarchy_name=hierarchy_path,
            markdown_docs_name=markdown_docs_path,
            ignore_list=[item.strip() for item in ignore_list.split(",") if item],
            language=language,
            log_level=log_level,
            model=model,
            temperature=temperature,
            request_timeout=request_timeout,
            openai_base_url=base_url,
            max_thread_count=max_thread_count,
        )
        set_logger_level_from_config(log_level=log_level)
    except ValidationError as e:
        handle_setting_error(e)
        return

    # 如果设置成功，则运行任务
    runner = Runner()
    runner.run()
    logger.success("文档任务完成。")
    if print_hierarchy:
        runner.meta_info.target_repo_hierarchical_tree.print_recursive()
        logger.success("层次结构已打印。")


def clean():
    """清理文档生成过程中创建的假文件。"""
    delete_fake_files()
    logger.success("假文件已清理。")


def diff():
    """检查更改并打印将更新或生成的文档。"""
    try:
        # 使用 SettingsManager 获取并验证设置
        setting = SettingsManager.get_setting()
    except ValidationError as e:
        handle_setting_error(e)
        return

    runner = Runner()
    if runner.meta_info.in_generation_process:  # 如果不是在生成过程中，就开始检测变更
        click.echo("此命令仅支持预检查")
        raise click.Abort()

    file_path_reflections, jump_files = make_fake_files()
    new_meta_info = MetaInfo.init_meta_info(file_path_reflections, jump_files)
    new_meta_info.load_doc_from_older_meta(runner.meta_info)
    delete_fake_files()

    DocItem.check_has_task(
        new_meta_info.target_repo_hierarchical_tree,
        ignore_list=setting.project.ignore_list,
    )
    if new_meta_info.target_repo_hierarchical_tree.has_task:
        click.echo("以下文档将生成/更新：")
        new_meta_info.target_repo_hierarchical_tree.print_recursive(
            diff_status=True, ignore_list=setting.project.ignore_list
        )
    else:
        click.echo("没有文档将生成/更新，请检查您的源代码更新")


def chat_with_repo():
    """启动与仓库的交互式聊天会话。"""
    try:
        # 使用 SettingsManager 获取并验证设置
        setting = SettingsManager.get_setting()
    except ValidationError as e:
        # 如果设置无效，处理配置错误
        handle_setting_error(e)
        return

    from repo_agent.chat_with_repo import main

    main()


if __name__ == "__main__":
    # 运行核心功能
    run()