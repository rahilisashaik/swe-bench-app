import React from 'react';
import './App.css';
import ProblemsTable from './components/ProblemsTable';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>SWE-bench Explorer</h1>
        <p>Browse and explore software engineering benchmark problems</p>
      </header>
      <main className="App-main">
        <ProblemsTable />
      </main>
    </div>
  );
}

export default App;

