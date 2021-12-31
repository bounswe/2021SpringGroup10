import React, { useState } from "react";

import "./styles.css";
import Header from "./header";

export const Homepage = () => {

    const [posts, setPosts] = useState([]);
    


    return (
        <div className="App">
            <Header />


        </div>
    );
}

export default Homepage;
