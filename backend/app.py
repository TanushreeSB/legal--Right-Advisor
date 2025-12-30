# backend/app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.dirname(__file__))

from hf_legal_analyzer import HFLegalAnalyzer

app = Flask(__name__, template_folder='../templates')
CORS(app)

# Global variable for analyzer
analyzer = None


def initialize_analyzer():
    """Initialize the REAL AI legal analyzer"""
    global analyzer
    try:
        print("🤖 Initializing Real AI Legal Analyzer...")
        
        # Use Hugging Face AI analyzer
        analyzer = HFLegalAnalyzer()
        print("✅ Real AI Legal Analyzer initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing AI analyzer: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_legal_issue():
    if not analyzer:
        return jsonify({'error': 'AI Analyzer not initialized. Please try again in a moment.'}), 500
    
    try:
        data = request.get_json()
        user_input = data.get('text', '')
        
        if not user_input:
            return jsonify({'error': 'Please provide some text to analyze'}), 400
        
        print(f"🔍 AI Analyzing: {user_input[:50]}...")
        
        # Analyze with REAL AI
        result = analyzer.analyze_with_ai(user_input)
        
        return jsonify({
            'success': True,
            'result': result,
            'ai_generated': result.get('ai_generated', False)
        })
    
    except Exception as e:
        return jsonify({'error': f'AI Analysis failed: {str(e)}'}), 500

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'ready' if analyzer else 'initializing',
        'message': 'AI Legal analyzer is ready!' if analyzer else 'Initializing AI legal analyzer...',
        'ai_enabled': True
    })

if __name__ == '__main__':
    print("🚀 Starting Right Advisor with REAL AI...")
    
    # Initialize analyzer
    if initialize_analyzer():
        print("🌐 Starting Flask server on http://localhost:5000")
        print("📱 AI-Powered Legal Assistant Ready!")
        app.run(debug=True, port=5000, host='0.0.0.0')
    else:
        print("❌ Failed to start server - AI analyzer initialization failed")

# Add to your existing app.py
from model_comparison import ModelComparison

# Initialize model comparison
model_comparison = ModelComparison()

@app.route('/api/compare-models', methods=['POST'])
def compare_models():
    try:
        data = request.get_json()
        user_input = data.get('text', '')
        
        if not user_input:
            return jsonify({'error': 'Please provide text to analyze'}), 400
        
        # Run model comparison
        comparison_result = model_comparison.compare_models(user_input)
        
        return jsonify({
            'success': True,
            'comparison': comparison_result,
            'model_stats': model_comparison.get_model_stats()
        })
    
    except Exception as e:
        return jsonify({'error': f'Model comparison failed: {str(e)}'}), 500


