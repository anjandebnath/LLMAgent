# src/agent_aj/app/agent.py
import comet_ml
import sys
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings
# --- FIX: Updated Qdrant import to resolve deprecation warning ---
from langchain_qdrant import Qdrant as QdrantVectorStore
from qdrant_client import QdrantClient
# --- FIX: Updated agent creation imports for ReAct agent ---
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools.render import render_text_description
# --- FIX: Updated GoogleSearchAPIWrapper import ---
from langchain_google_community import GoogleSearchAPIWrapper
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from agent_aj import config

class TravelAgent:
    def __init__(self):
        # Initialize Comet ML Experiment
        if config.COMET_API_KEY:
            self.experiment = comet_ml.Experiment(
                api_key=config.COMET_API_KEY,
                workspace=config.COMET_WORKSPACE,
                project_name=config.COMET_PROJECT_NAME
            )
        else:
            # Create a dummy experiment if no API key is provided
            print("⚠️ Comet ML API key not found. Running without experiment tracking.")
            self.experiment = comet_ml.OfflineExperiment()
        
        self.llm = OllamaLLM(model=config.LLM_MODEL, base_url=config.OLLAMA_BASE_URL)
        # --- FIX: The memory object is now managed manually, not by the agent executor ---
        self.memory = ConversationBufferWindowMemory(k=5, return_messages=True, memory_key="chat_history", input_key="input")
        
        # 1. Retriever for internal knowledge (Qdrant)
        try:
            embeddings = OllamaEmbeddings(model=config.EMBEDDING_MODEL, base_url=config.OLLAMA_BASE_URL)
            
            client = QdrantClient(
                host=config.QDRANT_HOST, 
                port=config.QDRANT_PORT
            )
            
            # --- FIX: Using updated QdrantVectorStore class ---
            vectorstore = QdrantVectorStore(
                client=client, 
                collection_name=config.QDRANT_COLLECTION_NAME, 
                embeddings=embeddings
            )
            
            self.retriever = vectorstore.as_retriever()
        except Exception as e:
            print(f"❌ Could not connect to or find Qdrant collection '{config.QDRANT_COLLECTION_NAME}'.")
            print(f"   Error: {e}")
            print("\n   Please ensure:")
            print("   1. Your Qdrant Docker container is running.")
            print("   2. You have successfully run 'feature_pipeline.py' to create the collection.")
            sys.exit(1) # Exit the script if we can't connect to the vector store

        # 2. Tool for external knowledge (Google Search)
        search = GoogleSearchAPIWrapper(
            google_api_key=config.GOOGLE_API_KEY,
            google_cse_id=config.GOOGLE_CSE_ID
        )
        search_tool = Tool(
            name="google_search",
            description="Search Google for recent travel information, weather, flight status, or other real-time data.",
            func=search.run,
        )

        # 3. Tool for internal knowledge retrieval
        retriever_tool = Tool(
            name="travel_package_retriever",
            description="Searches the travel package database to find deals, destinations, and descriptions.",
            func=self.retriever.invoke,
        )

        # Agent Setup
        self.tools = [search_tool, retriever_tool]
        
        # --- FIX: Switched to a ReAct agent prompt template ---
        react_prompt = PromptTemplate.from_template(
            """
            You are a helpful travel assistant. Answer the following questions as best you can.

            You have access to the following tools:
            {tools}

            Use the following format:

            Question: the input question you must answer
            Thought: you should always think about what to do
            Action: the action to take, should be one of [{tool_names}]
            Action Input: the input to the action
            Observation: the result of the action
            ... (this Thought/Action/Action Input/Observation can repeat N times)
            Thought: I now know the final answer
            Final Answer: the final answer to the original input question

            Begin!

            Previous conversation history:
            {chat_history}

            New Question: {input}
            Thought:{agent_scratchpad}
            """
        )

        # --- FIX: Create a ReAct agent, which is more compatible ---
        agent = create_react_agent(self.llm, self.tools, react_prompt)
        
        # --- FIX: Removed the 'memory' argument to prevent deprecation warning ---
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True, # As requested!
            handle_parsing_errors=True # More robust for production
        )

    def ask(self, question: str) -> str:
        """Main method to interact with the agent."""
        self.experiment.log_parameter("user_prompt", question)
        
        # --- FIX: Manually manage conversation history ---
        chat_history = self.memory.chat_memory.messages
        
        response = self.agent_executor.invoke({
            "input": question, 
            "chat_history": chat_history,
            "tools": render_text_description(self.tools),
            "tool_names": ", ".join([t.name for t in self.tools]),
        })
        
        output = response.get("output", "No output found.")
        
        # --- FIX: Manually save context to memory after invocation ---
        self.memory.save_context({"input": question}, {"output": output})
        
        self.experiment.log_text(output)
        return output

if __name__ == '__main__':
    print("--- Testing TravelAgent Class ---")
    # This creates an instance of your agent
    test_agent = TravelAgent()
    
    # --- Test Case 1: Internal Knowledge (Qdrant) ---
    print("\n[Test 1] Asking about internal data...")
    question1 = "What is the description for the trip to Paris?"
    response1 = test_agent.ask(question1)
    print(f">>> Response: {response1}")

    # --- Test Case 2: External Knowledge (Google Search) ---
    print("\n[Test 2] Asking a real-time question...")
    question2 = "What are the visa requirements for a US citizen traveling to Japan?"
    response2 = test_agent.ask(question2)
    print(f">>> Response: {response2}")
    
    # End the Comet experiment when done
    test_agent.experiment.end()
    print("\n--- Testing Finished ---")