import asyncio
import json
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

async def test_sentiment_mcp():
    """Test your deployed sentiment analysis MCP server"""
    endpoint = "https://sam522-demo-mcp-server.hf.space/gradio_api/mcp/sse"
    
    print("🧪 Testing your Sentiment Analysis MCP Server...")
    print(f"🔗 Endpoint: {endpoint}")
    print("-" * 60)
    
    try:
        async with sse_client(endpoint) as (read, write):
            session = ClientSession(read, write)
            await session.initialize()
            
            print("✅ Connected successfully!")
            
            # List available tools
            tools = await session.list_tools()
            print("\n📋 Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Test sentiment analysis with different types of text
            test_texts = [
                "I absolutely love this new AI technology! It's amazing!",
                "This is terrible and so frustrating. I hate it.",
                "The weather is okay today. Nothing special.",
                "AI will revolutionize how we work and live!",
                "I'm worried about the future of automation."
            ]
            
            print("\n🎭 Testing sentiment analysis:")
            print("=" * 60)
            
            for i, text in enumerate(test_texts, 1):
                print(f"\n{i}. Testing: '{text}'")
                
                try:
                    result = await session.call_tool('sentiment_analysis', {'text': text})
                    sentiment = json.loads(result.content[0].text)
                    
                    # Display results with nice formatting
                    polarity = sentiment['polarity']
                    subjectivity = sentiment['subjectivity']
                    assessment = sentiment['assessment']
                    
                    # Create visual indicators
                    polarity_bar = "📊 " + "🟢" * int((polarity + 1) * 5) + "🔴" * int((1 - polarity) * 5)
                    subjectivity_bar = "📈 " + "🔵" * int(subjectivity * 10)
                    
                    print(f"   Polarity: {polarity:+.2f} ({assessment})")
                    print(f"   {polarity_bar}")
                    print(f"   Subjectivity: {subjectivity:.2f}")
                    print(f"   {subjectivity_bar}")
                    
                except Exception as e:
                    print(f"   ❌ Error: {e}")
            
            print("\n" + "=" * 60)
            print("✅ All tests completed!")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check if your Hugging Face Space is running")
        print("   2. Verify the URL is correct")
        print("   3. Make sure gradio[mcp] is installed")

if __name__ == "__main__":
    asyncio.run(test_sentiment_mcp())