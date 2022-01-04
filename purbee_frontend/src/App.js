import logo from './logo.svg';
import LoginRegister from './components/login-register/login_register';
import ProfileInfo from './components/login-register/profile_info';
import Homepage from './components/homepage/homepage';
import Post from './components/post/post';
import CommunityHome from './components/community_page/community_home'
import CreatePostType from './components/createposttype/create_post_type'
import Feed from './components/feed/feed';
import Map from './components/post/googlemap';
import ProfilePage from './components/profile/profile_page'

import {
    BrowserRouter,
    Routes,
    Route,
    useNavigate,
} from "react-router-dom";
import CreatePost from './components/createpost/create_post';
import CreateCommunity from './components/createcommunity/create_community';

const asd = () => (<div>HELLOOOO</div>);

function App() {
    //let navigate = useNavigate();
    //const handleClick = () => {navigate("/invoices")}
  return (
      <div>
        <BrowserRouter>
          <Routes>
              <Route path="/create-community" element={<CreateCommunity />} />
              <Route path="/" element={<LoginRegister />} />
              <Route path="/home" element={<Homepage />} />
              <Route path="/profile-info" element={<ProfileInfo />} />
              <Route path="/community-home" element={<CommunityHome />} />
              <Route path="/create-post-type/:community_id" element={<CreatePostType />} />
              <Route path="/create-post/:community_id" element={<CreatePost />} />
              <Route path="/post" element={<Post />} />
              <Route path="/feed" element={<Feed id_list={["ba86cc3d-400e-401c-8b42-63402134cf62", "ba86cc3d-400e-401c-8b42-63402134cf62"]}/>} />
              <Route path="/map" element={<Map />} />
              <Route path ="/profile-page" element = {<ProfilePage />} />
          </Routes>
        </BrowserRouter> 
      </div>
  );
}

export default App;
