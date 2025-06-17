from gradio_client import Client

def test_gradio_connection():
    """Test the basic Gradio connection before running the smart agent"""
    print("🧪 Testing Gradio Connection")
    print("=" * 40)
    
    try:
        print("🔗 Connecting to your sentiment analysis server...")
        client = Client("https://sam522-demo-mcp-server.hf.space")
        print("✅ Connected successfully!")
        
        print("🧪 Testing sentiment analysis...")
        result = client.predict("I love this technology!", api_name="/predict")
        print(f"✅ Result: {result}")
        
        print("\n🎉 Connection test successful!")
        print("💡 You can now run the smart agent with confidence")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check if your Hugging Face Space is running")
        print("   2. Visit https://huggingface.co/spaces/sam522/demo_mcp_server in browser")
        print("   3. Wait for the Space to wake up (may take 30-60 seconds)")
        print("   4. Try again")
        
        return False

if __name__ == "__main__":
    if test_gradio_connection():
        print("\n🚀 Ready to run smart_sentiment_agent.py!")
    else:
        print("\n💔 Fix the connection issue before running the smart agent")