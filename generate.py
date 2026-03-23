import os
import requests
from datetime import datetime

# 1. 读取模板文件
with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

# 2. 构建提示词
today = datetime.now().strftime("%Y年%m月%d日")
prompt = f"""
你是一个专业的新闻编辑。请根据今日（{today}）最新的科技资讯，更新下面HTML模板中的内容。
要求：
1. 保持所有HTML标签、class、id、样式完全不变。
2. 只替换其中的文本内容（标题、日期、新闻列表、项目推荐等），确保数据真实、新鲜。
3. 日期部分请替换为今天：{today}。
4. 输出完整的HTML代码，不要添加任何额外解释。
5. 相关信息链接必须真实有效。

模板如下：
{template}
"""

# 3. 调用DeepSeek API
API_KEY = os.environ.get("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
payload = {
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.7,
    "max_tokens": 4000  # 根据你的模板长度调整
}

response = requests.post(API_URL, json=payload, headers=headers)
response.raise_for_status()
new_html = response.json()["choices"][0]["message"]["content"]

# 4. 保存为 index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("✅ 快报生成成功！")