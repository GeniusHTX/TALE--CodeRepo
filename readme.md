1. 进入主文件夹
    ```shell
    cd repo_agent
    ```
2. 将api配置到环境中
   ```shell
   export OPENAI_API_KEY=YOUR_API_KEY
   ```
3. 使用如下命令即可运行repoAgent
   ```shell
   python run.py --OPENAI_API_KEY your_api_key --model gpt-4o-mini --language Chinese
   ```
   相关配置可以根据需要在main_wh.py中修改, 默认参数如下:
   ```python
   def run(
    OPENAI_API_KEY: str,
    model="gpt-4o-mini",
    temperature=0.2,
    request_timeout=60,
    base_url="https://aigptx.top/v1",
    target_repo_path="/home/david/WH/projects/simdjson",  # 目标项目路径
    hierarchy_path=".project_doc_record",
    markdown_docs_path="markdown_docs",
    ignore_list="",
    language="English",
    max_thread_count=4,
    log_level="INFO",
    print_hierarchy=False,
    ):
   ```

   target_repo_path是目标项目路径，结果会自动生成在指定项目的markdown_docs_path下
   
4. 结合TALE需要在RepoAgent/repo_agent/chat_engine.py文件中的generate_doc方法中增加token估计与use less than xxx tokens，可以选择打开注释使用tale
    ```python
    # 打开注释可以使用zero-shot TALE
    # import copy
    # messages_copy = copy.deepcopy(messages)
    # messages_copy[-1].content = create_zero_shot_context()+messages_copy[-1].content
    # token_budget = extract_number(self.llm.chat(messages_copy).message.content)

    # messages[-1].content += f'use less than {token_budget}'
    ```
   
## 注意事项
OPENAI_API_KEY 是必填项目

不提供的参数将使用默认参数

你的本地/远程项目必须被git仓库记录

