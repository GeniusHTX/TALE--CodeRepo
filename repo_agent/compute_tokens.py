import json

total_prompt_tokens = 0
total_completion_tokens = 0
with open('/home/david/WH/RepoAgent/repo_agent/llm_response.jsonl','r') as f:
    for line in f:
        data = json.loads(line)
        total_prompt_tokens += data['LLM Prompt Tokens']
        total_completion_tokens += data['LLM Completion Tokens']
        
print(total_prompt_tokens)
print(total_completion_tokens)