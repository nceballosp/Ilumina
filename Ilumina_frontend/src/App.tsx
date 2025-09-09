import { Routes, Route } from 'react-router-dom';
import { Home } from './components/Home';
import { Load } from './components/Load';
import { Budget } from './components/Budget';
import { NavBar } from './components/Nav';

const App: React.FC = () => {
  return (
    <>
      <div>
        <NavBar></NavBar>
        <Routes>
          <Route path="" element={<Home title="" />} />
          <Route path="/load" element={<Load title="" />} />
          <Route path="/budget" element={<Budget title="" />} />
        </Routes>
      </div>
    </>
  );
};

export default App;
