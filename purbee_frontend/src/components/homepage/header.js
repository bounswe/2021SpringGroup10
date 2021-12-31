import * as React from 'react';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Grid from '@mui/material/Grid'
import { makeStyles } from '@mui/styles';
import { purple } from '@mui/material/colors';
import SideBar from "./sidebar";
import { useState } from "react";
import { Link } from 'react-router-dom';
import SearchBar from './searchbar';

const useStyles = makeStyles(() => ({
    root: {
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        paddingRight: "2%",
        paddingLeft: "2%",
        backgroundColor: purple[900],
        height: "4em"
    }

}))

export default function Header() {

    const classes = useStyles();
    const [open, setOpen] = useState(false);

    return (
        <>
            <SideBar open={open} setOpen={setOpen} />
            <Grid className={classes.root} >
                <Grid container>
                    <Grid
                        item
                        xs={4}
                        sm={4}
                        align="left"
                    >
                        <Link to="" style={{ textDecoration: 'none', color: "#101010" }} >
                            <p style={{ color: "#fff", fontWeight: "bolder", fontSize: "1.2vw" }}>
                                Purbee
                            </p>
                        </Link>
                    </Grid>

                    <Grid
                        item
                        xs={4}
                        sm={4}
                        align="center"
                    >
                        <SearchBar/>
                    </Grid>
                    <Grid
                        item
                        xs={4}
                        sm={4}
                        align="right"
                    >
                        <IconButton onClick={() => { setOpen(true) }}>
                            <MenuIcon style={{ color: "white" }} />
                        </IconButton>
                    </Grid>
                </Grid>
            </Grid>
        </>
    );
}