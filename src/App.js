import './App.css';
import {BrowserRouter as Router, Route,Routes} from 'react-router-dom';
import Home from './pages/Home';
import MindMap from './pages/MindMap';

function App() {
  return (
    <div className="App">
      <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/MindMap" element={<MindMap />} />
        </Routes>
      </div>
    </Router>
    </div>
  );
}

export default App;
