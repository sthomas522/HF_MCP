import asyncio
import json
from datetime import datetime
from gradio_client import Client

class FixedSmartSentimentAgent:
    """
    A working smart sentiment agent using the correct Gradio Client approach
    """
    
    def __init__(self):
        # Use the CORRECT URL - the main Gradio app, NOT the MCP endpoint
        self.space_url = "https://sam522-demo-mcp-server.hf.space"
        self.client = None
        self.conversation_history = []
        
    async def connect(self):
        """Connect to the sentiment analysis server"""
        try:
            print("🤖 Smart Sentiment Agent initializing...")
            print(f"🔗 Connecting to {self.space_url}")
            print("   (Using main Gradio app URL)")
            
            # Connect using the working method
            self.client = await asyncio.get_event_loop().run_in_executor(
                None, lambda: Client(self.space_url, verbose=False)
            )
            
            # Test the connection
            print("🧪 Testing connection...")
            test_result = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.client.predict("test", api_name="/predict")
            )
            
            print("✅ Connected successfully!")
            print("🧠 Smart sentiment-aware responses are ready!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            return False
    
    async def analyze_sentiment(self, text):
        """Analyze sentiment using Gradio Client"""
        try:
            if not self.client:
                raise Exception("Not connected")
            
            # Get sentiment analysis
            result = await asyncio.get_event_loop().run_in_executor(
                None, lambda: self.client.predict(text, api_name="/predict")
            )
            
            # Parse result
            sentiment_data = json.loads(result)
            sentiment_data['text'] = text
            sentiment_data['timestamp'] = datetime.now().isoformat()
            
            return sentiment_data
            
        except Exception as e:
            print(f"❌ Sentiment analysis failed: {e}")
            return None
    
    def generate_empathetic_response(self, sentiment_data, user_message):
        """Generate contextually appropriate responses based on sentiment"""
        if not sentiment_data:
            return "I'm here to help! Could you tell me more about what you're thinking?"
        
        polarity = sentiment_data['polarity']
        subjectivity = sentiment_data['subjectivity']
        assessment = sentiment_data['assessment']
        
        # Response templates based on sentiment
        if assessment == 'positive':
            if polarity > 0.3:
                responses = [
                    "🌟 I can feel your enthusiasm! That's wonderful to hear.",
                    "😊 Your positive energy is contagious! I'm excited to help.",
                    "✨ It sounds like you're in a great mood! How can I assist you today?"
                ]
            else:
                responses = [
                    "😌 I sense some gentle positivity in your message.",
                    "🙂 You seem content. I'm here if you need anything.",
                    "👍 That sounds pretty good! How can I help you further?"
                ]
        elif assessment == 'negative':
            if polarity < -0.3:
                responses = [
                    "😞 I can hear the frustration in your words. I'm here to help.",
                    "💙 That sounds really challenging. Let's work through this together.",
                    "🤗 I'm sorry you're dealing with this. How can I support you?"
                ]
            else:
                responses = [
                    "😐 I sense some concern in your message. I'm here to listen.",
                    "🤝 It sounds like you might be feeling uncertain. Let's talk about it.",
                    "💭 I notice some hesitation. Would you like to share more?"
                ]
        else:  # neutral
            responses = [
                "🤔 I'm listening. Please tell me more about what you need.",
                "📝 I understand. How would you like me to help you with this?",
                "💡 Got it. What specific assistance are you looking for?"
            ]
        
        base_response = responses[0]  # Use first response
        
        # Add subjectivity-based note
        if subjectivity > 0.7:
            emotion_note = " I can sense this is quite personal and important to you."
        elif subjectivity < 0.3:
            emotion_note = " Let's look at this objectively and find the best solution."
        else:
            emotion_note = ""
        
        return base_response + emotion_note
    
    def format_sentiment_display(self, sentiment):
        """Format sentiment for display"""
        if not sentiment:
            return "❌ No sentiment data"
        
        polarity = sentiment['polarity']
        subjectivity = sentiment['subjectivity']
        assessment = sentiment['assessment']
        
        # Visual indicators
        if assessment == 'positive':
            mood = "😊 Positive"
            color = "🟢"
        elif assessment == 'negative':
            mood = "😢 Negative"
            color = "🔴"
        else:
            mood = "😐 Neutral"
            color = "⚪"
        
        return f"{color} {mood} (polarity: {polarity:+.2f}, subjectivity: {subjectivity:.2f})"
    
    async def process_user_input(self, user_message, show_analysis=True):
        """Process user input with sentiment analysis and generate response"""
        print(f"\n💬 You: {user_message}")
        
        # Analyze sentiment
        sentiment = await self.analyze_sentiment(user_message)
        
        if show_analysis and sentiment:
            print(f"📊 Sentiment: {self.format_sentiment_display(sentiment)}")
        
        # Generate empathetic response
        response = self.generate_empathetic_response(sentiment, user_message)
        print(f"🤖 Agent: {response}")
        
        # Store in history
        self.conversation_history.append({
            'user_message': user_message,
            'sentiment': sentiment,
            'agent_response': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return response, sentiment
    
    def get_conversation_summary(self):
        """Get conversation sentiment summary"""
        if not self.conversation_history:
            return "No conversation data available."
        
        sentiments = [entry['sentiment'] for entry in self.conversation_history if entry['sentiment']]
        
        if not sentiments:
            return "No sentiment data available."
        
        avg_polarity = sum(s['polarity'] for s in sentiments) / len(sentiments)
        avg_subjectivity = sum(s['subjectivity'] for s in sentiments) / len(sentiments)
        
        assessments = [s['assessment'] for s in sentiments]
        pos_count = assessments.count('positive')
        neg_count = assessments.count('negative')
        neu_count = assessments.count('neutral')
        
        total = len(sentiments)
        
        return f"""
📊 Conversation Summary ({total} messages):
• Average Polarity: {avg_polarity:+.2f}
• Average Subjectivity: {avg_subjectivity:.2f}
• Positive: {pos_count} ({pos_count/total*100:.1f}%)
• Negative: {neg_count} ({neg_count/total*100:.1f}%)
• Neutral: {neu_count} ({neu_count/total*100:.1f}%)
        """.strip()
    
    async def interactive_chat(self):
        """Interactive chat with sentiment-aware responses"""
        print("\n" + "="*60)
        print("🤖 Smart Sentiment-Aware Agent")
        print("="*60)
        print("💬 Start chatting! I'll analyze sentiment and respond accordingly.")
        print("Commands: 'summary' for analysis, 'quit' to exit")
        print("-"*60)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n🤖 Agent: Thank you for the conversation! Take care! 👋")
                    break
                elif user_input.lower() == 'summary':
                    print(self.get_conversation_summary())
                    continue
                elif not user_input:
                    print("🤖 Agent: I'm here whenever you're ready to chat!")
                    continue
                
                # Process with sentiment analysis
                await self.process_user_input(user_input, show_analysis=True)
                
            except KeyboardInterrupt:
                print("\n\n🤖 Agent: Goodbye! 👋")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

async def quick_demo():
    """Quick demo of the smart agent"""
    agent = FixedSmartSentimentAgent()
    
    if not await agent.connect():
        return
    
    print("\n🧪 Quick Demo - Testing smart responses...")
    print("="*50)
    
    test_messages = [
        "I absolutely love this new technology!",
        "I'm really frustrated with this situation.",
        "The weather is okay today.",
        "I'm so excited about my new project!",
        "I'm worried about the future."
    ]
    
    for message in test_messages:
        await agent.process_user_input(message, show_analysis=True)
        await asyncio.sleep(1)  # Small delay for readability
    
    print("\n" + agent.get_conversation_summary())
    print("\n✅ Demo complete! The agent responds based on your sentiment.")

async def main():
    """Main function"""
    print("🎭 Fixed Smart Sentiment-Aware Agent")
    print("=" * 50)
    print("Choose mode:")
    print("1. Quick demo with examples")
    print("2. Interactive chat")
    
    choice = input("Enter 1 or 2 (default: 2): ").strip() or "2"
    
    if choice == "1":
        await quick_demo()
    else:
        agent = FixedSmartSentimentAgent()
        if await agent.connect():
            try:
                await agent.interactive_chat()
            finally:
                print("👋 Session ended")

if __name__ == "__main__":
    asyncio.run(main())