import React, { useState } from "react";

import "./styles.css";
import Header from "./header";
import Button from "@mui/material/Button";

export const Homepage = () => {

    const [posts, setPosts] = useState([]);
    


    return (
        <div className="App">
            <Header />


        </div>
    );
}

export default Homepage;
