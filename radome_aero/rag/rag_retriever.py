# radome_aero/rag/rag_retriever.py
import jieba
from pathlib import Path
import sys
sys.path.append(r"D:\AI_UAV_Radome")
from config import KNOWLEDGE_DIR

class KnowledgeRetriever:
    """知识库检索器：从本地知识库中检索相关内容"""
    
    def __init__(self, knowledge_dir=None):
        self.knowledge_dir = Path(knowledge_dir) if knowledge_dir else KNOWLEDGE_DIR
        self.docs = self._load_all_docs()
    
    def _load_all_docs(self):
        """加载所有知识库文档，按二级标题分段，检索更精准"""
        docs = []
        for file in self.knowledge_dir.glob("*.md"):
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                sections = content.split("## ")
                for i, section in enumerate(sections):
                    if i == 0:
                        title = file.stem
                        text = section
                    else:
                        lines = section.split("\n", 1)
                        title = lines[0].strip()
                        text = lines[1] if len(lines) > 1 else ""
                    docs.append({
                        "filename": file.name,
                        "title": title,
                        "content": f"## {title}\n{text}" if i > 0 else text,
                    })
        return docs
    
    def _calculate_similarity(self, query, text):
        """关键词相似度计算"""
        query_words = set(jieba.lcut(query))
        text_words = set(jieba.lcut(text))
        if not query_words:
            return 0
        common = query_words & text_words
        return len(common) / len(query_words)
    
    def retrieve(self, query, top_k=3):
        """检索最相关的前k条内容"""
        results = []
        for doc in self.docs:
            score = self._calculate_similarity(query, doc["content"])
            if score > 0:
                results.append({
                    "filename": doc["filename"],
                    "title": doc["title"],
                    "content": doc["content"],
                    "score": score
                })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    def get_context(self, query):
        """获取拼接好的上下文，直接给大模型用"""
        results = self.retrieve(query)
        if not results:
            return "无相关知识库内容"
        
        context = "【知识库参考内容】\n"
        for i, res in enumerate(results, 1):
            context += f"\n--- 参考{i}：{res['title']}（来自{res['filename']}） ---\n"
            context += res["content"]
        return context

if __name__ == "__main__":
    retriever = KnowledgeRetriever()
    print("测试检索：天线罩壁厚一般是多少？")
    print(retriever.get_context("天线罩壁厚一般是多少？"))