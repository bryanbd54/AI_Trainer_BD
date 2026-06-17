#!/bin/bash
set -e
cd "$(dirname "$0")"

# Use python3.13 if available (where deps are installed), else python3
PYTHON=$(command -v python3.13 || command -v python3)

# Install dependencies if needed
if ! $PYTHON -c "import anthropic, fastapi, uvicorn" 2>/dev/null; then
  echo "📦 Installing dependencies..."
  $PYTHON -m pip install -r requirements.txt -q
fi

echo ""
echo "🤖 Claude AI Trainer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Server starting at: http://localhost:8000"
echo "  Open this URL in your browser to play!"
if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo ""
  echo "  ⚠️  DEMO MODE — no API key set."
  echo "  Scoring is simulated. To enable real Claude:"
  echo "  export ANTHROPIC_API_KEY=your-key && ./start.sh"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

$PYTHON -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
