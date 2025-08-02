# agent_aj/main.py
from agent_aj.app.agent import TravelAgent

def main():
    print("🤖 Welcome to the AI Travel Agent CLI!")
    print("Ask me about our travel packages or any other travel-related questions.")
    print("Type 'exit' to quit.")
    
    agent = TravelAgent()
    
    while True:
        try:
            query = input("\n> You: ")
            if query.lower() == 'exit':
                print("👋 Goodbye!")
                agent.experiment.end() # End the Comet experiment
                break
            
            response = agent.ask(query)
            print(f"\n> Agent: {response}")
            
        except Exception as e:
            print(f"An error occurred: {e}")
            agent.experiment.end()
            break

if __name__ == "__main__":
    main()