import json
import requests
import re

def generate_report(article_url):
    # 定义API的URL
    api_url = "https://api.coze.cn/v1/workflow/run"

    # 定义请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer token"
    }

    # 检查article_url是否为文章链接
    if not re.match(r'^https?://', article_url):
        print("Error: 无效的文章链接")
        return None

    # 定义请求体
    data = {
        "parameters": {
            "article_url": article_url
        },
        "workflow_id": "7456817920665387023"
    }

    # 发送POST请求到API
    response = requests.post(api_url, headers=headers, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        result = response.json()
        # Step 1: Parse the outer JSON
        outer_data = json.loads(result["data"])

        # Step 2: Extract and clean the inner JSON string
        inner_json_str = outer_data["data"]
        inner_json_str = inner_json_str.replace("```json\n", "").replace("\n```", "")

        # Step 3: Parse the inner JSON string
        try:
            summary_data = json.loads(inner_json_str)
            print(summary_data)
        except json.JSONDecodeError as e:
            print(f"JSON decode error at position {e.pos}: {e}")
            print(f"Context: {inner_json_str[e.pos-20:e.pos+20]}")
            summary_data = {}

        return {
            "标题": summary_data["title"],
            "标签": summary_data["tags"],
            "一句话总结": summary_data["summary"],
            "详细摘要": summary_data["detailed_summary"],
            "本文解决问题": summary_data["problems_solved"],
            "优先级评分": summary_data["priority_score"],
            "文章大纲": summary_data["outline"]
        }
    else:
        # 处理错误
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    article_url = 'https://mp.weixin.qq.com/s/5hCYC7SPcQ9Vp2GwdAGb5w'
    report = generate_report(article_url)
    print(report)
