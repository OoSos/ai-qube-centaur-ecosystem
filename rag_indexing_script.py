import os
import weaviate

def index_knowledge_sources(weaviate_url, sources):
    client = weaviate.Client(weaviate_url)
    for source in sources:
        for root, _, files in os.walk(source):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                obj = {
                    'file_path': file_path,
                    'content': content
                }
                client.data_object.create(obj, "KnowledgeSource")
                print(f"Indexed: {file_path}")

if __name__ == "__main__":
    # Update with your actual Weaviate instance URL
    WEAVIATE_URL = "http://localhost:8080"
    knowledge_sources = [
        "project_documentation/",
        "agent_interaction_logs/",
        "successful_task_patterns/",
        "user_preferences/",
        "code_quality_standards/",
        "performance_benchmarks/"
    ]
    index_knowledge_sources(WEAVIATE_URL, knowledge_sources)
