import React, { useState, useEffect } from 'react';
import './ProblemsTable.css';

const API_BASE = 'http://localhost:5000/api';

function ProblemsTable() {
  const [problems, setProblems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [datasetName, setDatasetName] = useState('princeton-nlp/SWE-bench');
  const [split, setSplit] = useState('test');
  const [limit, setLimit] = useState(100);
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);
  const [hasMore, setHasMore] = useState(false);

  useEffect(() => {
    loadProblems();
  }, [datasetName, split, limit, offset]);

  const loadProblems = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `${API_BASE}/problems?dataset_name=${encodeURIComponent(datasetName)}&split=${split}&limit=${limit}&offset=${offset}`
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      setProblems(data.problems);
      setTotal(data.total);
      setHasMore(data.has_more);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePrevious = () => {
    if (offset > 0) {
      setOffset(Math.max(0, offset - limit));
    }
  };

  const handleNext = () => {
    if (hasMore) {
      setOffset(offset + limit);
    }
  };

  const handleProblemClick = (instanceId) => {
    alert(`Problem detail view coming soon!\nInstance ID: ${instanceId}\n\nThis will show the IDE view with code editor.`);
  };

  if (loading && problems.length === 0) {
    return (
      <div className="loading-container">
        <div className="loading">Loading problems...</div>
      </div>
    );
  }

  return (
    <div className="problems-table-container">
      <div className="controls">
        <div className="control-group">
          <label htmlFor="dataset-name">Dataset:</label>
          <select
            id="dataset-name"
            value={datasetName}
            onChange={(e) => {
              setDatasetName(e.target.value);
              setOffset(0);
            }}
          >
            <option value="princeton-nlp/SWE-bench">SWE-bench (Full)</option>
            <option value="SWE-bench/SWE-bench_Lite">SWE-bench Lite</option>
            <option value="SWE-bench/SWE-bench_Verified">SWE-bench Verified</option>
          </select>
        </div>

        <div className="control-group">
          <label htmlFor="split">Split:</label>
          <select
            id="split"
            value={split}
            onChange={(e) => {
              setSplit(e.target.value);
              setOffset(0);
            }}
          >
            <option value="test">Test</option>
            <option value="train">Train</option>
            <option value="dev">Dev</option>
          </select>
        </div>

        <div className="control-group">
          <label htmlFor="limit">Limit:</label>
          <input
            type="number"
            id="limit"
            value={limit}
            min="10"
            max="1000"
            step="10"
            onChange={(e) => {
              setLimit(parseInt(e.target.value));
              setOffset(0);
            }}
          />
        </div>
      </div>

      {error && (
        <div className="error">
          Error: {error}
        </div>
      )}

      {total > 0 && (
        <div className="stats">
          Showing {offset + 1}-{Math.min(offset + limit, total)} of {total} problems
        </div>
      )}

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Instance ID</th>
              <th>Repository</th>
              <th>Problem Statement</th>
              <th>Version</th>
              <th>Created At</th>
              <th>Patch</th>
              <th>Test Patch</th>
            </tr>
          </thead>
          <tbody>
            {problems.map((problem) => (
              <tr
                key={problem.instance_id}
                onClick={() => handleProblemClick(problem.instance_id)}
                className="problem-row"
              >
                <td>
                  <span className="instance-id">{problem.instance_id}</span>
                </td>
                <td>
                  <span className="repo">{problem.repo}</span>
                </td>
                <td>
                  <div className="problem-statement">{problem.problem_statement}</div>
                </td>
                <td>{problem.version || 'N/A'}</td>
                <td>{problem.created_at || 'N/A'}</td>
                <td>
                  <span className={`badge ${problem.has_patch ? 'badge-yes' : 'badge-no'}`}>
                    {problem.has_patch ? 'Yes' : 'No'}
                  </span>
                </td>
                <td>
                  <span className={`badge ${problem.has_test_patch ? 'badge-yes' : 'badge-no'}`}>
                    {problem.has_test_patch ? 'Yes' : 'No'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {total > limit && (
        <div className="pagination">
          <button
            onClick={handlePrevious}
            disabled={offset === 0}
          >
            Previous
          </button>
          <span className="pagination-info">
            Page {Math.floor(offset / limit) + 1} of {Math.ceil(total / limit)}
          </span>
          <button
            onClick={handleNext}
            disabled={!hasMore}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}

export default ProblemsTable;

