import React from "react";
import ReactDOM from "react-dom";

import "./styles.css";
import {Link as RouterLink} from "react-router-dom";
import Button from "@mui/material/Button";

export const Homepage = () => {
    return (
        <div style={{margin: "350px 250px 350px 250px", position: "relative"}}>
            <div style={{color: "#FFF"}}>
                <h1 style={{color: "#fff"}}>
                    Website
                    <br />
                    Coming Soon
                </h1>
                <Button
                    variant="outlined"
                    color="primary"
                    className="form__custom-button">
                    <RouterLink to="/community-home"> Community Home </RouterLink>
                </Button>
                <Button
                    variant="outlined"
                    color="primary"
                    className="form__custom-button">
                    <RouterLink to="/create-post-type"> Create Post Type </RouterLink>
                </Button>
                <Button
                    variant="outlined"
                    color="primary"
                    className="form__custom-button">
                    <RouterLink to="/create-post"> Create Post </RouterLink>
                </Button>
                <Button
                    variant="outlined"
                    color="primary"
                    className="form__custom-button">
                    <RouterLink to="/post"> Post </RouterLink>
                </Button>
            </div>
        </div>
    );
}

export default Homepage;
