"""
Flask API server for SWE-bench application
"""
import sys
from pathlib import Path

backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from flask import Flask, jsonify, request
from flask_cors import CORS
from api.api import get_raw_swe_bench_hf
import json

app = Flask(__name__)
CORS(app)
_dataset_cache = {}


def get_dataset(dataset_name="princeton-nlp/SWE-bench", split="test"):
    """Get dataset with caching"""
    cache_key = f"{dataset_name}_{split}"
    if cache_key not in _dataset_cache:
        _dataset_cache[cache_key] = get_raw_swe_bench_hf(dataset_name, split)
    return _dataset_cache[cache_key]


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})


@app.route('/api/problems', methods=['GET'])
def get_problems():
    """
    Get list of problems (tabular data)
    Query params:
        - dataset_name: Dataset name (default: princeton-nlp/SWE-bench)
        - split: Dataset split (default: test)
        - limit: Limit number of results (default: 100)
        - offset: Offset for pagination (default: 0)
    """
    dataset_name = request.args.get('dataset_name', 'princeton-nlp/SWE-bench')
    split = request.args.get('split', 'test')
    limit = int(request.args.get('limit', 100))
    offset = int(request.args.get('offset', 0))
    
    try:
        dataset = get_dataset(dataset_name, split)
        
        # Convert to list and extract relevant fields for table
        problems = []
        end_idx = min(offset + limit, len(dataset))
        
        for i in range(offset, end_idx):
            item = dataset[i]
            problems.append({
                'instance_id': item['instance_id'],
                'repo': item['repo'],
                'problem_statement': item['problem_statement'][:500] + '...' if len(item.get('problem_statement', '')) > 500 else item.get('problem_statement', ''),
                'base_commit': item.get('base_commit', ''),
                'version': item.get('version', ''),
                'created_at': item.get('created_at', ''),
                'has_patch': bool(item.get('patch')),
                'has_test_patch': bool(item.get('test_patch')),
            })
        
        return jsonify({
            'problems': problems,
            'total': len(dataset),
            'offset': offset,
            'limit': limit,
            'has_more': end_idx < len(dataset)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/problems/<instance_id>', methods=['GET'])
def get_problem_detail(instance_id):
    """
    Get detailed information about a specific problem
    Query params:
        - dataset_name: Dataset name (default: princeton-nlp/SWE-bench)
        - split: Dataset split (default: test)
    """
    dataset_name = request.args.get('dataset_name', 'princeton-nlp/SWE-bench')
    split = request.args.get('split', 'test')
    
    try:
        dataset = get_dataset(dataset_name, split)
        
        # Find the problem by instance_id
        problem = None
        for item in dataset:
            if item['instance_id'] == instance_id:
                problem = dict(item)
                break
        
        if not problem:
            return jsonify({'error': f'Problem {instance_id} not found'}), 404
        
        return jsonify(problem)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

