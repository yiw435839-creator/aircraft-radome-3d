# rag_demo.py
import time
from radome_aero.rag.rag_retriever import KnowledgeRetriever
from radome_aero.llm_client.deepseek_api import generate_radome_code
from config import GENERATED_CODE_DIR

def main():
    print("="*60)
    print("🚀 航空天线罩AI智能设计系统 v1.0")
    print("="*60)
    
    # 1. 初始化知识库
    print("\n📚 正在加载航空设计知识库...")
    retriever = KnowledgeRetriever()
    print(f"✅ 知识库加载完成，共{len(retriever.docs)}条设计规范")
    
    # 2. 用户输入需求
    requirement = input("\n请输入天线罩设计需求：\n")
    
    # 3. 检索知识库
    print("\n🔍 正在检索相关设计规范...")
    context = retriever.get_context(requirement)
    print("✅ 检索完成")
    
    # 4. 生成建模代码
    print("\n🤖 正在生成参数化建模代码（请耐心等待60秒）...")
    try:
        code = generate_radome_code(requirement, context)
    except Exception as e:
        print(f"\n❌ 接口调用失败：{e}")
        print("💡 解决办法：切换手机热点重试、多运行几次")
        return
        
    print("✅ 代码生成完成")
    
    # 5. 保存代码
    time_str = time.strftime("%Y%m%d_%H%M%S")
    save_file = GENERATED_CODE_DIR / f"radome_model_{time_str}.py"
    with open(save_file, "w", encoding="utf-8") as f:
        f.write(code)

    # 6. 输出结果
    print("\n" + "="*60)
    print("📝 生成的FreeCAD建模代码：")
    print("="*60)
    print(code)
    print("="*60)
    print(f"\n💾 代码已保存至：{save_file}")
    print("💡 使用方法：复制代码到FreeCAD Python控制台运行即可生成三维模型")
    print("💡 运行后会自动输出重量、表面积等工程参数")

if __name__ == "__main__":
    main()