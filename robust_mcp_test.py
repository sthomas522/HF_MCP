import asyncio
import json
import aiohttp
import time
from datetime import datetime

async def test_http_endpoint_first():
    """Test if the basic HTTP endpoint is working"""
    endpoint = "https://sam522-demo-mcp-server.hf.space"
    
    print("🌐 Step 1: Testing basic HTTP connectivity...")
    
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(endpoint) as response:
                print(f"✅ Base URL Status: {response.status}")
                print(f"📋 Content Type: {response.headers.get('content-type', 'unknown')}")
                
                if response.status == 200:
                    return True
                else:
                    print(f"❌ Unexpected status code: {response.status}")
                    return False
                    
    except asyncio.TimeoutError:
        print("❌ HTTP request timed out (10 seconds)")
        return False
    except Exception as e:
        print(f"❌ HTTP test failed: {e}")
        return False

async def test_sse_endpoint():
    """Test the SSE endpoint directly"""
    sse_endpoint = "https://sam522-demo-mcp-server.hf.space/gradio_api/mcp/sse"
    
    print("\n🔄 Step 2: Testing SSE endpoint...")
    
    try:
        timeout = aiohttp.ClientTimeout(total=15)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(sse_endpoint) as response:
                print(f"📡 SSE Status: {response.status}")
                print(f"📋 SSE Content Type: {response.headers.get('content-type', 'unknown')}")
                
                if response.status != 200:
                    print(f"❌ SSE endpoint returned status: {response.status}")
                    return False
                
                # Read first few lines with timeout
                print("📥 Reading SSE stream (max 10 seconds)...")
                start_time = time.time()
                line_count = 0
                
                async for line in response.content:
                    if time.time() - start_time > 10:  # 10 second timeout
                        print("⏰ SSE read timeout reached")
                        break
                        
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line:
                        print(f"  📨 {decoded_line}")
                        line_count += 1
                        if line_count >= 5:  # Read max 5 lines
                            break
                
                if line_count > 0:
                    print("✅ SSE endpoint is streaming data correctly")
                    return True
                else:
                    print("❌ No data received from SSE endpoint")
                    return False
                    
    except asyncio.TimeoutError:
        print("❌ SSE request timed out")
        return False
    except Exception as e:
        print(f"❌ SSE test failed: {e}")
        return False

async def test_gradio_api_directly():
    """Test Gradio API directly without MCP"""
    api_endpoint = "https://sam522-demo-mcp-server.hf.space/api/predict"
    
    print("\n🎯 Step 3: Testing Gradio API directly...")
    
    try:
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            
            # Test payload for sentiment analysis
            payload = {
                "data": ["I love this technology!"],
                "fn_index": 0
            }
            
            async with session.post(api_endpoint, json=payload) as response:
                print(f"🎯 API Status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ API Response: {result}")
                    
                    # Try to parse the sentiment result
                    if 'data' in result and len(result['data']) > 0:
                        sentiment_json = result['data'][0]
                        sentiment_data = json.loads(sentiment_json)
                        print(f"📊 Parsed Sentiment: {sentiment_data}")
                        return True
                    else:
                        print("❌ Unexpected API response format")
                        return False
                else:
                    print(f"❌ API returned status: {response.status}")
                    response_text = await response.text()
                    print(f"Response: {response_text[:200]}...")
                    return False
                    
    except asyncio.TimeoutError:
        print("❌ API request timed out")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

async def test_mcp_connection_with_timeout():
    """Test MCP connection with proper timeout handling"""
    print("\n🔌 Step 4: Testing MCP connection...")
    
    try:
        # Import MCP libraries with error handling
        try:
            from mcp.client.session import ClientSession
            from mcp.client.sse import sse_client
        except ImportError as e:
            print(f"❌ MCP library import failed: {e}")
            print("💡 Try: pip install mcp gradio[mcp]")
            return False
        
        endpoint = "https://sam522-demo-mcp-server.hf.space/gradio_api/mcp/sse"
        
        print(f"🔗 Connecting to: {endpoint}")
        print("⏰ Timeout: 30 seconds")
        
        # Use asyncio.wait_for to add timeout
        async def connect_with_timeout():
            async with sse_client(endpoint) as (read, write):
                session = ClientSession(read, write)
                await session.initialize()
                
                print("✅ MCP connection established!")
                
                # Test listing tools
                print("📋 Listing available tools...")
                tools_response = await session.list_tools()
                
                if tools_response and tools_response.tools:
                    print(f"✅ Found {len(tools_response.tools)} tools:")
                    for tool in tools_response.tools:
                        print(f"  • {tool.name}: {tool.description}")
                    
                    # Test calling a tool
                    print("\n🧪 Testing sentiment analysis...")
                    test_text = "I love this new technology!"
                    result = await session.call_tool('sentiment_analysis', {'text': test_text})
                    
                    if result and result.content:
                        sentiment_json = result.content[0].text
                        sentiment_data = json.loads(sentiment_json)
                        print(f"✅ Sentiment analysis successful!")
                        print(f"   Text: '{test_text}'")
                        print(f"   Result: {sentiment_data}")
                        return True
                    else:
                        print("❌ Tool call returned no results")
                        return False
                else:
                    print("❌ No tools found")
                    return False
        
        # Run with timeout
        result = await asyncio.wait_for(connect_with_timeout(), timeout=30.0)
        return result
        
    except asyncio.TimeoutError:
        print("❌ MCP connection timed out after 30 seconds")
        return False
    except Exception as e:
        print(f"❌ MCP connection failed: {e}")
        return False

async def comprehensive_test():
    """Run all tests in sequence"""
    print("🚀 Comprehensive MCP Server Test")
    print("=" * 60)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        ("Basic HTTP connectivity", test_http_endpoint_first),
        ("SSE endpoint", test_sse_endpoint),
        ("Gradio API direct", test_gradio_api_directly),
        ("MCP connection", test_mcp_connection_with_timeout)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 40)
        
        start_time = time.time()
        try:
            success = await test_func()
            end_time = time.time()
            duration = end_time - start_time
            
            results.append((test_name, success, duration))
            
            if success:
                print(f"✅ {test_name} passed ({duration:.2f}s)")
            else:
                print(f"❌ {test_name} failed ({duration:.2f}s)")
                
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            results.append((test_name, False, duration))
            print(f"💥 {test_name} crashed: {e} ({duration:.2f}s)")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for test_name, success, duration in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:8} {test_name:25} ({duration:.2f}s)")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your MCP server is working correctly.")
    elif passed > 0:
        print("⚠️  Some tests passed. Check failed tests above.")
    else:
        print("💔 All tests failed. Check your server deployment.")
    
    print(f"\n🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

async def quick_test():
    """Quick test that skips potentially slow operations"""
    print("⚡ Quick MCP Server Test")
    print("=" * 40)
    
    # Test 1: Basic connectivity
    if not await test_http_endpoint_first():
        print("💔 Basic connectivity failed. Server may be down.")
        return
    
    # Test 2: Try Gradio API directly (faster than MCP)
    if await test_gradio_api_directly():
        print("\n✅ Your server is working! The Gradio API responds correctly.")
        print("💡 If MCP connection fails, it might be a client-side issue.")
    else:
        print("\n❌ Server has issues. Check your Hugging Face Space.")

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Quick test (faster, basic checks)")
    print("2. Comprehensive test (slower, all features)")
    
    choice = input("Enter 1 or 2 (default: 1): ").strip() or "1"
    
    if choice == "2":
        asyncio.run(comprehensive_test())
    else:
        asyncio.run(quick_test())