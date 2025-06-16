import gradio as gr

def letter_counter(word: str, letter: str) -> int:
    """
    Count the number of occurrences of a letter in a word or text.

    Args:
        word (str): The input text to search through
        letter (str): The letter to search for

    Returns:
        int: The number of times the letter appears in the text
    """
    if not word or not letter:
        return 0
    
    word = word.lower()
    letter = letter.lower()
    count = word.count(letter)
    return count

def word_stats(text: str) -> dict:
    """
    Get comprehensive statistics about a text.
    
    Args:
        text (str): The input text to analyze
        
    Returns:
        dict: Statistics including word count, character count, etc.
    """
    if not text:
        return {"words": 0, "characters": 0, "letters": 0, "sentences": 0}
    
    words = len(text.split())
    characters = len(text)
    letters = sum(1 for c in text if c.isalpha())
    sentences = text.count('.') + text.count('!') + text.count('?')
    
    return {
        "words": words,
        "characters": characters,
        "letters": letters,
        "sentences": sentences
    }

# Create a standard Gradio interface with multiple tabs
with gr.Blocks(title="Text Analysis MCP Server") as demo:
    gr.Markdown("# Text Analysis Tools")
    gr.Markdown("This server provides text analysis functions via both web interface and MCP.")
    
    with gr.Tab("Letter Counter"):
        with gr.Row():
            text_input = gr.Textbox(
                label="Enter text",
                placeholder="Type your text here...",
                lines=3
            )
            letter_input = gr.Textbox(
                label="Enter letter to count",
                placeholder="e.g., 'a'",
                max_lines=1
            )
        
        count_output = gr.Number(label="Letter count")
        count_btn = gr.Button("Count Letters", variant="primary")
        
        count_btn.click(
            fn=letter_counter,
            inputs=[text_input, letter_input],
            outputs=count_output
        )
    
    with gr.Tab("Text Statistics"):
        stats_text_input = gr.Textbox(
            label="Enter text to analyze",
            placeholder="Type your text here...",
            lines=5
        )
        stats_output = gr.JSON(label="Text Statistics")
        stats_btn = gr.Button("Analyze Text", variant="primary")
        
        stats_btn.click(
            fn=word_stats,
            inputs=stats_text_input,
            outputs=stats_output
        )
    
    with gr.Tab("MCP Info"):
        gr.Markdown("""
        ## MCP Server Information
        
        This server is running as an MCP (Model Context Protocol) server.
        
        **MCP Endpoint**: `http://127.0.0.1:7860/gradio_api/mcp/sse`
        
        **Available Functions**:
        - `letter_counter`: Count occurrences of a letter in text
        - `word_stats`: Get comprehensive text statistics
        
        **Usage with MCP Client**:
        ```json
        {
            "model": "your-model",
            "provider": "your-provider",
            "servers": [
                {
                    "type": "sse",
                    "config": {
                        "url": "http://127.0.0.1:7860/gradio_api/mcp/sse"
                    }
                }
            ]
        }
        ```
        """)

# Launch both the Gradio web interface and the MCP server
if __name__ == "__main__":
    print("🚀 Starting Text Analysis Server...")
    print("📊 Gradio Interface: http://127.0.0.1:7860")
    print("🔌 MCP Server: http://127.0.0.1:7860/gradio_api/mcp/sse")
    print("💡 Use the Gradio interface to test functions")
    print("🤖 Use the MCP endpoint with tiny-agents or other MCP clients")
    
    demo.launch(
        mcp_server=True,
        server_name="127.0.0.1",
        server_port=7860,
        show_api=True
    )