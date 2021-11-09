import * as React from 'react';

import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

export default function LoginPage(){
    const[user_name, set_user_name] = React.useState("");
    const[password, set_password] = React.useState("");
    const[password_repeat, set_password_repeat] = React.useState("");
    const[mail_address, set_mail_address] = React.useState("");
    const[login_or_register, set_login_or_register] = React.useState("login");

    const handle_user_name_change = (event)  => set_user_name(event.target.value);
    const handle_password_change = (event) => set_password(event.target.value);
    const handle_password_repeat_change = (event) => set_password_repeat(event.target.value);
    const handle_mail_address_change = (event) => set_mail_address(event.target.value);
    const handle_login_or_register_change = (event) => set_login_or_register(event.target.value);

    const button_clicked = () => {
        //make api call
    }
    const password_match = () => password === password_repeat;


    return (<div>
            {
                login_or_register === "login" ?
                    <div>
                        <Box
                            component="form"
                            sx={{
                                '& .MuiTextField-root': { m: 1, width: '25ch' },
                            }}
                            noValidate
                            autoComplete="off">
                            <div>
                                <TextField
                                    required
                                    id="user_name"
                                    label="User Name"
                                    value={user_name}
                                    onChange={handle_user_name_change}
                                />
                                <TextField
                                    required
                                    type="password"
                                    id="password"
                                    label="Password"
                                    value={password}
                                    onChange={handle_password_change}
                                />
                            </div>
                        </Box>
                    </div>
                    :
                    <div>
                        <Box
                            component="form"
                            sx={{
                                '& .MuiTextField-root': { m: 1, width: '25ch' },
                            }}
                            noValidate
                            autoComplete="off">
                            <div>
                                <div>
                                    <TextField
                                        required
                                        id="user_name"
                                        label="User Name"
                                        value={user_name}
                                        onChange={handle_user_name_change}
                                    />
                                    <TextField
                                        required
                                        id="mail_address"
                                        label="Mail Address"
                                        value={mail_address}
                                        onChange={handle_mail_address_change}
                                    />
                                </div>
                                <div>
                                    <TextField
                                        required
                                        error={password_match}
                                        type="password"
                                        id="password"
                                        label="Password"
                                        value={password}
                                        onChange={handle_password_change}
                                    />
                                    <TextField
                                        required
                                        error={password_match}
                                        type="password"
                                        id="password_repeat"
                                        label="Password Repeat"
                                        value={password_repeat}
                                        onChange={handle_password_repeat_change}
                                    />
                                </div>
                            </div>
                        </Box>
                    </div>
            }
            <ToggleButtonGroup
                color="primary"
                value={login_or_register}
                exclusive
                onChange={handle_login_or_register_change}
            >
                <ToggleButton value="login">Login</ToggleButton>
                <ToggleButton value="register">Register</ToggleButton>
            </ToggleButtonGroup>
            <div>
                <Button
                    variant="outlined"
                    onClick={button_clicked}
                >{login_or_register.toUpperCase()+"!"}
                </Button>
            </div>
        </div>


    )
}