import logo from './logo.svg';
import LoginRegister from './components/login-register/login_register';
import ProfileInfo from './components/login-register/profile_info';
import Homepage from './components/homepage/homepage';
import CommunityHome2 from './components/community_page/community_home'

import {
    BrowserRouter,
    Routes,
    Route,
    useNavigate,
} from "react-router-dom";

const asd = () => (<div>HELLOOOO</div>);

function App() {
    //let navigate = useNavigate();
    //const handleClick = () => {navigate("/invoices")}
  return (
      <div>
        <BrowserRouter>
          <Routes>
              <Route path="/" element={<LoginRegister />} />
              <Route path="/home" element={<Homepage />} />
              <Route path="/profile-info" element={<ProfileInfo />} />
              <Route path="/community-home" element={<CommunityHome2 />} />
          </Routes>
        </BrowserRouter>
      </div>
  );
}

export default App;
