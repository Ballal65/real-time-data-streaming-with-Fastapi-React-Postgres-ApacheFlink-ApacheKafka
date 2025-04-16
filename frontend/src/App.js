import { Route, Routes } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Example from './pages/Example';
import Project from './pages/Project';
import JreDashboard from './pages/JreDashboard';
import Certificates from './pages/Certificates';
import NiftyDashboard from './pages/NiftyDashboard';
function App() {

  return (
    <Routes>
      <Route path="/crud" element={<Dashboard/>} />    
      <Route path="/example" element={<Example/>} />  
      <Route path="/project" element={<Project/>} /> 
      <Route path="/jre-dashboard" element={<JreDashboard/>} /> 
      <Route path="/" element={<Certificates/>} />
      <Route path='/nifty-dashboard' element={<NiftyDashboard/>} />
    </Routes>
  );
}

export default App;
