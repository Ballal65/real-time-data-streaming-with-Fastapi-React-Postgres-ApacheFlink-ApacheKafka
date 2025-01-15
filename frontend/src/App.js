import { Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Example from './pages/Example';
import Project from './pages/Project';
function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard/>} />    
      <Route path="/example" element={<Example/>} />  
      <Route path="/project" element={<Project/>} /> 
    </Routes>
  );
}

export default App;
