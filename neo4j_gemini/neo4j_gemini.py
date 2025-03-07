from langchain_google_vertexai import ChatVertexAI, VertexAIEmbeddings
from langchain_community.vectorstores import Neo4jVector
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
from google.cloud import aiplatform
from tenacity import retry, wait_random_exponential
import vertexai
import os
load_dotenv()
# Initialize Gemini
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
from google import genai
from google.genai import types
vertexai.init(    project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
    location="us-central1",
    # Options:
    # - "dedicated": Use Provisioned Throughput
    # - "shared": Use pay-as-you-go
    # https://cloud.google.com/vertex-ai/generative-ai/docs/use-provisioned-throughput
    request_metadata=[("x-vertex-ai-llm-request-type", "shared")],
)

client = genai.Client(api_key=GOOGLE_API_KEY)
MODEL_ID = "gemini-2.0-flash"
response = client.models.generate_content(
    model = MODEL_ID,
    contents="Cypher code to fetch all nodes"
)

print(response.text)

llm = ChatVertexAI(
    model_name=MODEL_ID,
    max_output_tokens=1024,
    temperature=0.1,
    top_p=0.8,
    top_k=40
)

# Set up Neo4j connection
# https://bb440c21.databases.neo4j.io/db/neo4j/query/v2
neo4j_url = "neo4j+s://"+os.getenv("neo4j_db")+".databases.neo4j.io/"
print(neo4j_url)
graph = Neo4jGraph(
    url=neo4j_url,
    username="neo4j",
    password=os.getenv("neo4j_pwd")
)
query = "MATCH (n:Person) RETURN n LIMIT 5"
results = graph.query(query)
print(results)

# Create GraphCypherQAChain
chain = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    verbose=True, 
    allow_dangerous_requests=True
)
#     request_metadata=[("x-vertex-ai-llm-request-type", "shared")],

# Run a query
# result = chain.run("create a relationship called Is_Related_to between Bob and Alice")
# print(result)
result = chain.run("fetch all nodes")
print(result)


