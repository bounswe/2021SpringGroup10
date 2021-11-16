import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import './styles.css'
import DatePicker from '@mui/lab/DatePicker';
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import FileBase64 from 'react-file-base64';
import {Link as RouterLink}from "react-router-dom";

export default function ProfileInfo() {
    const [first_name, set_first_name] = React.useState("");
    const [last_name, set_last_name] = React.useState("");
    const [bio, set_bio] = React.useState("");
    const [birth_date, set_birth_date] = React.useState("");
    const [photo, set_photo] = React.useState("https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg");

    const handle_save = () => {
        //TODO
    }
    const handle_skip = () => {
        //TODO
    }

    return (
        <div className="App">
            <form className="form">
                <img src={photo} style={{ width: "25%", alignSelf: "center", paddingBottom: "0.8em" }}></img>

                <h4 style={{ alignSelf: "baseline" }}>First Name: </h4>
                <div style={{ height: "0.8em" }}></div>
                <TextField
                    id="first_name"
                    formControlProps={{
                        fullWidth: true
                    }}
                    type="text"
                    onChange={(e) => set_first_name(e.target.value)}
                />
                <div style={{ height: "0.8em" }}></div>
                <h4 style={{ alignSelf: "baseline" }}>Last Name:</h4>
                <div style={{ height: "0.8em" }}></div>
                <TextField
                    id="last_name"
                    formControlProps={{
                        fullWidth: true
                    }}
                    onChange={(e) => set_last_name(e.target.value)}
                />

                <div style={{ height: "0.8em" }}></div>
                <h4 style={{ alignSelf: "baseline" }}>Birth Date:</h4>
                <div style={{ height: "0.8em" }}></div>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                    <DatePicker
                        value={birth_date}
                        onChange={(newValue) => {
                            set_birth_date(newValue);
                        }}
                        renderInput={(params) => <TextField {...params} />}
                    />
                </LocalizationProvider>
                <div style={{ height: "0.8em" }}></div>
                <h4 style={{ alignSelf: "baseline" }}>Bio:</h4>
                <div style={{ height: "0.8em" }}></div>
                <TextField
                    id="bio"
                    multiline={true}
                    minRows="5"
                    formControlProps={{
                        fullWidth: true
                    }}
                    onChange={(e) => set_bio(e.target.value)}
                />
                <div style={{ height: "0.8em" }}></div>
                <h4 style={{ alignSelf: "baseline" }}>Profile Picture:</h4>
                <div style={{ height: "0.8em" }}></div>
                <FileBase64
                    multiple={false}
                    onDone={(t) => {set_photo(t.base64)}} />
                <Button
                    variant="contained"
                    color="primary"
                    className="form__custom-button"
                    onClick={handle_save}>
                    <RouterLink to="/home"> Save </RouterLink>
                </Button>
                <Button
                    variant="contained"
                    color="primary"
                    className="form__custom-button"
                    onClick={handle_skip}>
                    <RouterLink to="/home"> Skip </RouterLink>
                </Button>
            </form>


        </div >
    )
}