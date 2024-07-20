import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import UploadPage from './components/UploadPage';
// import AddPosition from './components/AddPosition';
import Apply from './components/Apply';
import HrDashboard from './components/HrDashboard';
import Test from './components/test';

function App() {
  return (
    <Router>
    <Routes>
      {/* <Route path={"/"} element={<UploadPage/>}/> */}
      {/* <Route path={"/newposition"} element={<AddPosition/>}/> */}
      <Route path={"/apply"} element={<Apply/>}/>
      <Route path={"/hr"} element={<HrDashboard/>}/>
      <Route path={"/test"} element={<Test/>}/>
       
      </Routes>
  </Router>
  );
}

export default App;
