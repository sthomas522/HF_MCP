import asyncio
import json
from datetime import datetime
from gradio_client import Client

class WorkingSentimentClient:
    """
    A working sentiment analysis client using Gradio Client
    (bypasses MCP connection issues)
    """
    
    def __init__(self, space_url="https://sam522-demo-mcp-server.hf.space"):
        self.space_url = space_url
        self.client = None
        self.analysis_history = []
        
    def connect(self):
        """Connect to the Gradio server"""
        try:
            print(f"🔗 Connecting to {self.space_url}...")
            self.client = Client(self.space_url)
            print("✅ Connected successfully!")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using the working Gradio Client method"""
        try:
            if not self.client:
                raise Exception("Not connected. Call connect() first.")
            
            # Use the working prediction method
            result = self.client.predict(text, api_name="/predict")
            
            # Parse the JSON result
            sentiment_data = json.loads(result)
            
            # Add metadata
            sentiment_data['text'] = text
            sentiment_data['timestamp'] = datetime.now().isoformat()
            
            # Store in history
            self.analysis_history.append(sentiment_data)
            
            return sentiment_data
            
        except Exception as e:
            print(f"❌ Sentiment analysis failed: {e}")
            return None
    
    def analyze_batch(self, texts):
        """Analyze multiple texts"""
        results = []
        
        print(f"📊 Analyzing {len(texts)} texts...")
        
        for i, text in enumerate(texts, 1):
            print(f"  {i}/{len(texts)}: Processing...")
            sentiment = self.analyze_sentiment(text)
            if sentiment:
                results.append(sentiment)
        
        return results
    
    def format_result(self, sentiment):
        """Format sentiment result for display"""
        if not sentiment:
            return "❌ No sentiment data"
        
        polarity = sentiment['polarity']
        subjectivity = sentiment['subjectivity']
        assessment = sentiment['assessment']
        
        # Create emoji and visual indicators
        if assessment == 'positive':
            mood_emoji = "😊"
            color = "🟢"
        elif assessment == 'negative':
            mood_emoji = "😢"
            color = "🔴"
        else:
            mood_emoji = "😐"
            color = "⚪"
        
        # Create polarity bar
        polarity_normalized = (polarity + 1) / 2  # Convert -1,1 to 0,1
        bar_length = 20
        filled_length = int(polarity_normalized * bar_length)
        polarity_bar = "█" * filled_length + "░" * (bar_length - filled_length)
        
        # Create subjectivity bar
        subj_filled = int(subjectivity * bar_length)
        subj_bar = "█" * subj_filled + "░" * (bar_length - subj_filled)
        
        return f"""
{mood_emoji} Sentiment Analysis Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Text: "{sentiment['text']}"
{color} Assessment: {assessment.upper()}
📊 Polarity: {polarity:+.2f} [{polarity_bar}] ({polarity:+.2f})
📈 Subjectivity: {subjectivity:.2f} [{subj_bar}] ({subjectivity:.2f})
⏰ Analyzed: {sentiment['timestamp']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """.strip()
    
    def get_summary(self):
        """Get summary of all analyses"""
        if not self.analysis_history:
            return "No analysis history available."
        
        polarities = [s['polarity'] for s in self.analysis_history]
        subjectivities = [s['subjectivity'] for s in self.analysis_history]
        assessments = [s['assessment'] for s in self.analysis_history]
        
        avg_polarity = sum(polarities) / len(polarities)
        avg_subjectivity = sum(subjectivities) / len(subjectivities)
        
        pos_count = assessments.count('positive')
        neg_count = assessments.count('negative')
        neu_count = assessments.count('neutral')
        
        total = len(self.analysis_history)
        
        return f"""
📊 Sentiment Analysis Summary ({total} texts analyzed)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 Average Polarity: {avg_polarity:+.2f}
📉 Average Subjectivity: {avg_subjectivity:.2f}

📋 Sentiment Distribution:
  😊 Positive: {pos_count} ({pos_count/total*100:.1f}%)
  😢 Negative: {neg_count} ({neg_count/total*100:.1f}%)
  😐 Neutral:  {neu_count} ({neu_count/total*100:.1f}%)

💡 Overall Mood: {'😊 Generally Positive' if avg_polarity > 0.1 else '😢 Generally Negative' if avg_polarity < -0.1 else '😐 Balanced'}
🎭 Emotional Tone: {'High' if avg_subjectivity > 0.6 else 'Moderate' if avg_subjectivity > 0.3 else 'Low'} subjectivity
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """.strip()

def interactive_demo():
    """Interactive demo of the working sentiment client"""
    print("🎭 Working Sentiment Analysis Client")
    print("=" * 60)
    
    client = WorkingSentimentClient()
    
    if not client.connect():
        print("💔 Failed to connect to the server")
        return
    
    print("✅ Connected! Ready for sentiment analysis")
    print("\nCommands:")
    print("  • Type text to analyze sentiment")
    print("  • 'batch' for multiple text analysis")
    print("  • 'summary' for analysis statistics")
    print("  • 'examples' for sample texts")
    print("  • 'quit' to exit")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n💬 Enter text (or command): ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
                
            elif user_input.lower() == 'summary':
                print(client.get_summary())
                
            elif user_input.lower() == 'batch':
                print("📝 Enter texts to analyze (empty line to finish):")
                texts = []
                while True:
                    text = input(f"  Text {len(texts)+1}: ").strip()
                    if not text:
                        break
                    texts.append(text)
                
                if texts:
                    results = client.analyze_batch(texts)
                    for result in results:
                        print(client.format_result(result))
                        
            elif user_input.lower() == 'examples':
                examples = [
                    "I absolutely love this new AI technology!",
                    "This is terrible and so frustrating.",
                    "The weather is okay today.",
                    "AI will revolutionize how we work!",
                    "I'm worried about privacy implications."
                ]
                
                print("🧪 Analyzing example texts...")
                results = client.analyze_batch(examples)
                for result in results:
                    print(client.format_result(result))
                    
            elif user_input:
                # Analyze the input text
                sentiment = client.analyze_sentiment(user_input)
                print(client.format_result(sentiment))
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n👋 Thanks for using the sentiment analyzer!")

def quick_test():
    """Quick test of the client"""
    print("⚡ Quick Sentiment Analysis Test")
    print("=" * 40)
    
    client = WorkingSentimentClient()
    
    if not client.connect():
        return
    
    test_texts = [
        "I love this new technology!",
        "This is awful and disappointing.",
        "The product is okay, nothing special.",
        "Outstanding customer service!",
        "The interface could be better."
    ]
    
    print("🧪 Testing with sample texts...")
    results = client.analyze_batch(test_texts)
    
    for result in results:
        print(client.format_result(result))
    
    print(client.get_summary())

def main():
    """Main function"""
    print("🎯 Working Sentiment Analysis Client")
    print("=" * 50)
    print("Choose mode:")
    print("1. Quick test with examples")
    print("2. Interactive mode")
    
    choice = input("Enter 1 or 2 (default: 2): ").strip() or "2"
    
    if choice == "1":
        quick_test()
    else:
        interactive_demo()

if __name__ == "__main__":
    main()