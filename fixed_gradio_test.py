import asyncio
import json
import aiohttp
import time
from datetime import datetime

async def discover_gradio_endpoints():
    """Discover available Gradio endpoints"""
    base_url = "https://sam522-demo-mcp-server.hf.space"
    
    print("🔍 Step 2: Discovering Gradio API endpoints...")
    
    # Common Gradio API endpoints to try
    endpoints_to_try = [
        f"{base_url}/api/predict",      # Old format
        f"{base_url}/call/predict",     # New format
        f"{base_url}/run/predict",      # Alternative
        f"{base_url}/api/v1/predict",   # Versioned API
        f"{base_url}/gradio_api/predict", # Custom path
    ]
    
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            # First, try to get API info
            info_endpoints = [
                f"{base_url}/info",
                f"{base_url}/config",
                f"{base_url}/api",
                f"{base_url}/api/v1/info"
            ]
            
            print("📋 Checking for API info...")
            for info_url in info_endpoints:
                try:
                    async with session.get(info_url) as response:
                        if response.status == 200:
                            info = await response.json()
                            print(f"✅ Found API info at: {info_url}")
                            print(f"📊 API Info: {json.dumps(info, indent=2)[:300]}...")
                            
                            # Look for endpoints in the info
                            if 'named_endpoints' in info:
                                print("🎯 Available endpoints:")
                                for endpoint, details in info['named_endpoints'].items():
                                    print(f"  • {endpoint}: {details}")
                            
                            return info
                            
                except Exception as e:
                    print(f"❌ {info_url}: {e}")
                    continue
            
            print("⚠️  No API info found, trying direct endpoints...")
            return None
            
    except Exception as e:
        print(f"❌ Error discovering endpoints: {e}")
        return None

async def test_gradio_client_api():
    """Test using Gradio Client library"""
    print("\n🎯 Step 3: Testing with Gradio Client...")
    
    try:
        # Try importing gradio_client
        try:
            from gradio_client import Client
        except ImportError:
            print("❌ gradio_client not installed")
            print("💡 Try: pip install gradio_client")
            return False
        
        print("🔗 Connecting with Gradio Client...")
        client = Client("https://sam522-demo-mcp-server.hf.space")
        
        # Test the prediction
        test_text = "I love this new technology!"
        print(f"🧪 Testing with text: '{test_text}'")
        
        result = await asyncio.get_event_loop().run_in_executor(
            None, 
            lambda: client.predict(test_text, api_name="/predict")
        )
        
        print(f"✅ Gradio Client result: {result}")
        
        # Try to parse as sentiment data
        if isinstance(result, str):
            try:
                sentiment_data = json.loads(result)
                print(f"📊 Parsed sentiment: {sentiment_data}")
                return True
            except json.JSONDecodeError:
                print(f"⚠️  Result is not JSON: {result}")
                return True  # Still counts as success
        else:
            print(f"✅ Got result: {result}")
            return True
            
    except Exception as e:
        print(f"❌ Gradio Client test failed: {e}")
        return False

async def test_manual_api_calls():
    """Test various API endpoint formats"""
    base_url = "https://sam522-demo-mcp-server.hf.space"
    
    print("\n🎯 Step 4: Testing manual API calls...")
    
    # Different payload formats to try
    payloads = [
        {
            "data": ["I love this technology!"],
            "fn_index": 0
        },
        {
            "data": ["I love this technology!"]
        },
        {
            "inputs": ["I love this technology!"]
        },
        {
            "text": "I love this technology!"
        }
    ]
    
    # Different endpoints to try
    endpoints = [
        f"{base_url}/api/predict",
        f"{base_url}/call/predict",
        f"{base_url}/run/predict",
        f"{base_url}/predict",
        f"{base_url}/api/v1/predict"
    ]
    
    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            for endpoint in endpoints:
                print(f"\n🔗 Trying endpoint: {endpoint}")
                
                for i, payload in enumerate(payloads):
                    try:
                        print(f"  📤 Payload {i+1}: {payload}")
                        
                        async with session.post(endpoint, json=payload) as response:
                            print(f"  📡 Status: {response.status}")
                            
                            if response.status == 200:
                                result = await response.json()
                                print(f"  ✅ Success! Response: {result}")
                                
                                # Try to parse sentiment if it's a string
                                if 'data' in result and len(result['data']) > 0:
                                    data = result['data'][0]
                                    if isinstance(data, str):
                                        try:
                                            sentiment = json.loads(data)
                                            print(f"  📊 Sentiment: {sentiment}")
                                        except:
                                            print(f"  📄 Raw data: {data}")
                                
                                return True
                            else:
                                error_text = await response.text()
                                print(f"  ❌ Error: {error_text[:100]}...")
                                
                    except Exception as e:
                        print(f"  💥 Request failed: {e}")
                        continue
            
            print("❌ All manual API attempts failed")
            return False
            
    except Exception as e:
        print(f"❌ Manual API test failed: {e}")
        return False

async def test_mcp_with_better_error_handling():
    """Test MCP with improved error handling"""
    print("\n🔌 Step 5: Testing MCP connection (improved)...")
    
    try:
        from mcp.client.session import ClientSession
        from mcp.client.sse import sse_client
    except ImportError as e:
        print(f"❌ MCP import failed: {e}")
        print("💡 Try: pip install mcp")
        return False
    
    endpoint = "https://sam522-demo-mcp-server.hf.space/gradio_api/mcp/sse"
    
    try:
        print(f"🔗 Connecting to MCP: {endpoint}")
        
        # Test with timeout
        async def mcp_test():
            async with sse_client(endpoint) as (read, write):
                print("  ✅ SSE connection established")
                
                session = ClientSession(read, write)
                print("  🔄 Initializing session...")
                
                await session.initialize()
                print("  ✅ Session initialized")
                
                # List tools
                print("  📋 Listing tools...")
                tools = await session.list_tools()
                
                if tools and tools.tools:
                    print(f"  ✅ Found {len(tools.tools)} tools:")
                    for tool in tools.tools:
                        print(f"    • {tool.name}: {tool.description}")
                    
                    # Test tool call
                    print("  🧪 Testing sentiment analysis...")
                    result = await session.call_tool(
                        'sentiment_analysis', 
                        {'text': 'I love this!'}
                    )
                    
                    if result and result.content:
                        sentiment_json = result.content[0].text
                        sentiment = json.loads(sentiment_json)
                        print(f"  ✅ MCP tool call successful: {sentiment}")
                        return True
                    else:
                        print("  ❌ No result from tool call")
                        return False
                else:
                    print("  ❌ No tools found")
                    return False
        
        return await asyncio.wait_for(mcp_test(), timeout=30.0)
        
    except asyncio.TimeoutError:
        print("❌ MCP connection timed out")
        return False
    except Exception as e:
        print(f"❌ MCP test failed: {e}")
        print(f"   Error type: {type(e)}")
        return False

async def comprehensive_gradio_test():
    """Run comprehensive test of your Gradio MCP server"""
    print("🚀 Comprehensive Gradio MCP Server Test")
    print("=" * 60)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test 1: Basic connectivity
    print("🌐 Step 1: Testing basic connectivity...")
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get("https://sam522-demo-mcp-server.hf.space") as response:
                if response.status == 200:
                    print("✅ Server is accessible")
                else:
                    print(f"❌ Server returned status: {response.status}")
                    return
    except Exception as e:
        print(f"❌ Cannot reach server: {e}")
        return
    
    # Run all tests
    tests = [
        ("API Discovery", discover_gradio_endpoints),
        ("Gradio Client", test_gradio_client_api),
        ("Manual API Calls", test_manual_api_calls),
        ("MCP Connection", test_mcp_with_better_error_handling)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        try:
            success = await test_func()
            results.append((test_name, success))
            
            if success:
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
                
        except Exception as e:
            print(f"💥 {test_name} CRASHED: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 FINAL SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Result: {passed}/{total} tests passed")
    
    if passed >= 1:
        print("🎉 Your server is working! At least one connection method succeeded.")
        print("💡 You can use the successful method for your MCP clients.")
    else:
        print("💔 All tests failed. Check your Hugging Face Space deployment.")

if __name__ == "__main__":
    # Install required packages
    print("📦 Note: This test requires 'gradio_client' package")
    print("   Install with: pip install gradio_client")
    print()
    
    asyncio.run(comprehensive_gradio_test())