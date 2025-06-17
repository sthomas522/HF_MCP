# HF_MCP

export SSL_CERT_FILE=$(python -m certifi)
export REQUESTS_CA_BUNDLE=$(python -m certifi)
export CURL_CA_BUNDLE=$(python -m certifi)

tiny-agents run sentiment_agent.json
