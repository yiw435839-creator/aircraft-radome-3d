"""
AeroCAD Copilot AI云端流水线
输入文字需求 → DeepSeek解析参数 → 纯净CAD代码 → 建模导出STEP
"""
from radome_aero.llm_client.deepseek_api import get_design_scheme, generate_freecad_code

def run_workflow(text):
    print("===== 1. AI解析整流罩尺寸 =====")
    params = get_design_scheme(text)
    print(params)

    print("\n===== 2. 生成FreeCAD建模代码 =====")
    cad_code = generate_freecad_code(params)
    print(cad_code)
    print("\n操作：复制全部代码，打开FreeCAD软件，底部控制台粘贴运行，生成模型后导出STEP到output文件夹")

if __name__ == "__main__":
    user_req = "DA42机头GPS天线罩，壁厚2mm"
    run_workflow(user_req)