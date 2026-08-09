# radome_aero/llm_client/deepseek_api.py
import os
from dotenv import load_dotenv
from openai import OpenAI
import sys
sys.path.append(r"D:\AI_UAV_Radome")
from config import OUTPUT_DIR

# 加载.env密钥
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    timeout=60.0
)

def generate_radome_code(requirement, knowledge_context):
    """
    结合知识库生成FreeCAD天线罩建模代码，带工程计算功能
    """
    prompt = f"""
你是专业的航空结构设计AI助手，精通FreeCAD参数化建模。
请根据用户的设计需求，结合知识库参考内容，生成可直接运行的FreeCAD天线罩建模代码。

【用户需求】
{requirement}

【知识库参考】
{knowledge_context}

【⚠️ 强制代码规范（必须100%严格遵守，否则运行失败）】
1. 必须使用参数化文档特征建模，禁止使用Part.makeEllipsoid()等底层函数：
   - 椭球：doc.addObject("Part::Ellipsoid", "名字")
   - 圆柱/孔：doc.addObject("Part::Cylinder", "名字")
   - 长方体法兰：doc.addObject("Part::Box", "名字")
   - 布尔合并：doc.addObject("Part::Fuse", "名字")
   - 布尔切除：doc.addObject("Part::Cut", "名字")
   - 每一步创建完必须执行 doc.recompute()

2. 坐标系统一规则（绝对不能错）：
   - 椭球中心必须在 Z = radius_z 高度，底部刚好落在Z=0平面
   - 法兰顶面必须在Z=0平面，向下延伸，厚度为flange_height
   - 安装孔必须是**垂直方向**（不旋转！），从下往上贯穿法兰和壳体底部
   - 安装孔必须沿**正圆**均匀分布，用同一个分布圆半径

3. 抽壳必须用「外椭球减内椭球」的方式，禁止用makeThickness

4. 必须包含工程计算功能：
   - 计算模型体积、重量（玻璃钢密度1.9g/cm³）
   - 计算外表面积
   - 最后打印输出所有工程参数

5. Windows系统路径，所有文件保存到 D:\AI_UAV_Radome\output 目录，禁止用/tmp

6. 显示规则：
   - 所有中间特征全部隐藏，只显示最终完整模型
   - 最后必须执行这两行：
     Gui.activeView().viewAxonometric()
     Gui.SendMsgToActiveView("ViewFit")

7. 代码开头必须导入：import FreeCAD as App, import FreeCADGui as Gui, import Part, import math, import os

8. 只输出纯Python代码，不要markdown格式，不要```标记，不要多余解释

直接输出代码：
"""
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是专业的航空结构设计工程师，代码必须严格遵守坐标规范，运行后直接显示完整模型，并输出工程参数。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=4000
    )
    
    # 自动清理markdown标记
    code = response.choices[0].message.content.strip()
    if code.startswith("```python"):
        code = code[9:]
    if code.endswith("```"):
        code = code[:-3]
    return code.strip()