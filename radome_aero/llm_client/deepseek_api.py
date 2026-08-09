import os
from dotenv import load_dotenv
from openai import OpenAI

# 读取环境变量
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)

def get_design_scheme(user_requirement: str) -> str:
    """用户需求解析尺寸参数"""
    prompt = f"""
你是民航航空整流罩专业设计师，依据需求输出DA42天线罩全部尺寸：
长轴长度、短轴宽度、罩体高度、壳体壁厚、法兰宽度、螺栓孔直径、安装孔偏移距离，单位mm
只返回参数文本，不要多余文字
需求：{user_requirement}
"""
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return resp.choices[0].message.content.strip()


def generate_freecad_code(param_text: str) -> str:
    """生成纯净FreeCAD代码，不带markdown代码框"""
    code_prompt = f"""
根据天线罩参数编写可直接运行的FreeCAD Python代码：
1. 自动新建文档，运行结束关闭文档
2. 椭球形外壳+底部法兰+四个安装螺栓孔
3. STEP文件保存到项目output文件夹
4. 仅输出纯Python代码，禁止```python、```、文字介绍
参数：{param_text}
"""
    resp = client.chat.completions.create(
        model="deepseek-coder",
        messages=[{"role": "user", "content": code_prompt}],
        temperature=0.2
    )
    return resp.choices[0].message.content.strip()


# 自测入口
if __name__ == "__main__":
    test = "DA42机头GPS天线罩，壁厚2mm"
    print(get_design_scheme(test))