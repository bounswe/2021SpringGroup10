import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import './styles.css'
import { Card } from '@mui/material';
import Link from '@mui/material/Link';
import {Link as RouterLink}from "react-router-dom";

export default function LoginPage() {
    const [user_name, set_username] = React.useState("");
    const [password, set_password] = React.useState("");
    const [first_name, set_first_name] = React.useState("");
    const [last_name, set_last_name] = React.useState("");
    const [password_repeat, set_password_repeat] = React.useState("");
    const [mail_address, set_mail_address] = React.useState("");
    const [login_or_register, set_login_or_register] = React.useState("login");
    const [password_match, set_password_match] = React.useState(true)

    const handle_username_change = (event) => set_username(event.target.value);
    const handle_password_change = (event) => set_password(event.target.value);
    const handle_password_repeat_change = (event) => set_password_repeat(event.target.value);
    const handle_mail_address_change = (event) => set_mail_address(event.target.value);
    const handle_login_or_register_change = (value) => set_login_or_register(value);

    const signin = () => {
        // TODO
    }

    const signup = () => {
        // TODO
    }

    React.useEffect(() => {
        set_password_match(password === password_repeat)
    }, [password, password_repeat])

    return login_or_register == "login"
        ? (
            <div className="App">
                <form className="form">
                    <img src="https://i.ibb.co/SXprk2W/2.png" style={{ width: "25%", alignSelf: "center", paddingBottom: "0.8em" }}></img>

                    <h4 style={{ alignSelf: "baseline" }}>Email</h4>
                    <div style={{ height: "0.8em" }}></div>
                    <TextField
                        id="email"
                        formControlProps={{
                            fullWidth: true
                        }}
                        type="text"
                        onChange={handle_username_change}
                    />
                    <div style={{ height: "0.8em" }}></div>
                    <h4 style={{ alignSelf: "baseline" }}>Password</h4>
                    <div style={{ height: "0.8em" }}></div>
                    <TextField
                        id="password"
                        formControlProps={{
                            fullWidth: true
                        }}
                        type="password"
                        onChange={handle_password_change}
                    />

                    <Button 
                        variant="contained" 
                        color="primary" 
                        className="form__custom-button"
                        onClick={signin}>
                        <RouterLink to="/profile-info"> Log in </RouterLink>
                    </Button>
                    <div style={{ height: "1em" }}></div>
                    <div style={{ backgroundColor: "#fff", alignSelf: "center" }}>
                        New to Purbee?
                        <Link
                            component="button"
                            variant="body2"
                            onClick={handle_login_or_register_change}
                        > Sign up
                        </Link>
                    </div>
                </form>


            </div >)
        : (
            <div className="App">
                <form className="form">
                    <img src="https://i.ibb.co/SXprk2W/2.png" style={{ width: "25%", alignSelf: "center", paddingBottom: "0.8em" }}></img>

                    <h4 style={{ alignSelf: "baseline" }}>Email</h4>
                    <div style={{ height: "0.8em" }}></div>
                    <TextField
                        id="email"
                        formControlProps={{
                            fullWidth: true
                        }}
                        type="text"
                        onChange={handle_username_change}
                    />
                    <div style={{ height: "0.8em" }}></div>
                    <h4 style={{ alignSelf: "baseline" }}>Username</h4>
                    <div style={{ height: "0.8em" }}></div>
                    <TextField
                        id="username"
                        formControlProps={{
                            fullWidth: true
                        }}
                        type="text"
                        onChange={handle_username_change}
                    />
                    <div style={{ height: "0.8em" }}></div>
                    <h4 style={{ alignSelf: "baseline" }}>Password</h4>
                    <div style={{ height: "0.8em" }}></div>
                    <TextField
                        id="password"
                        formControlProps={{
                            fullWidth: true
                        }}
                        type="password"
                        onChange={handle_password_change}
                    />
                    <div style={{ height: "0.8em" }}></div>
                    <h4 style={{ alignSelf: "baseline" }}>Repeat Password</h4>
                    <div style={{ height: "0.8em" }}></div>
                    <TextField
                        id="password_repeat"
                        formControlProps={{
                            fullWidth: true
                        }}
                        type="password"
                        error={!password_match}
                        onChange={handle_password_repeat_change}
                    />

                    <Button variant="contained" color="primary" className="form__custom-button">
                        <RouterLink to="/profile-info"> Sign up </RouterLink>
                    </Button>
                    <div style={{ height: "1em" }}></div>
                    <div style={{ backgroundColor: "#fff", alignSelf: "center", display: "flex", justifyContent: "space-between" }}>
                        Already have an account? 
                        <Link
                            component="button"
                            variant="body2"
                            onClick={handle_login_or_register_change}
                        > Sign in
                        </Link>
                    </div>
                </form>
                
            </div>
        )
}