from langchain_google_vertexai import ChatVertexAI, VertexAIEmbeddings
from langchain_community.vectorstores import Neo4jVector
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
import os
load_dotenv()
# Initialize Gemini
'''
- Passing a constructor argument
- Using vertexai.init()
- Setting project using 'gcloud config set project my-project'
- Setting a GCP environment variable
- To create a Google Cloud project, please follow guidance at https://developers.google.com/workspace/guides/create-project

llm = ChatVertexAI(
    model_name="gemini-1.5-pro-001",
    max_output_tokens=1024,
    temperature=0.1,
    top_p=0.8,
    top_k=40
)
'''
# Set up Neo4j connection
# https://bb440c21.databases.neo4j.io/db/neo4j/query/v2
neo4j_url = "neo4j+s://"+os.getenv("neo4j_db")+".databases.neo4j.io/"
print(neo4j_url)
graph = Neo4jGraph(
    url=neo4j_url,
    username="neo4j",
    password=os.getenv("neo4j_pwd")
)
create_query = """
CREATE (p:Person {name: 'Alice', age: 30})
RETURN p
"""
result = graph.query(create_query)
print(result)

query = "MATCH (n:Person) RETURN n LIMIT 5"
results = graph.query(query)
print(results)

'''
# Create GraphCypherQAChain
chain = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    verbose=True
)

# Run a query
result = chain.run("fetch all nodes")
print(result)
'''

