import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeIcon from '@mui/icons-material/Home';
import PersonIcon from '@mui/icons-material/Person';
import { makeStyles } from '@mui/styles';
import { Link } from 'react-router-dom';
import { purple } from '@mui/material/colors';
import { getUser } from '../../utils/common';
import PeopleIcon from '@mui/icons-material/People';
import LogoutIcon from '@mui/icons-material/Logout';
import Logout from '@mui/icons-material/Logout';
import { removeUserSession } from '../../utils/common';
import { useParams, useNavigate } from 'react-router-dom'

const useStyles = makeStyles(() => ({
    root: {
        overflowX: "hidden",
        overflowY: "hidden"
    },
    drawerHead: {
        color: "#fff",
        backgroundColor: purple[900],
        height: "3.6em",
    }
}))

export const SideBar = (props) => {

    
    let navigate = useNavigate()
    const logout = () => {
        removeUserSession();
        navigate('/')
    }

    const classes = useStyles();

    return (
        <Drawer
            open={props.open}
            anchor="right"
            onClose={() => { props.setOpen(false) }}
            className={classes.root}
        >
            <ListItem className={classes.drawerHead}>
                <ListItemText primary={"Purbee"} />
            </ListItem>
            <List>
                <Link to="/home" style={{ textDecoration: 'none', color: "#101010" }} >
                    <ListItem button >
                        <ListItemIcon >
                            <HomeIcon />
                        </ListItemIcon>
                        <ListItemText primary={"Home"} />
                    </ListItem>
                </Link>
                <Divider />

                <Link to={"/profile-page/" + getUser()} style={{ textDecoration: 'none', color: "#101010" }} >
                    <ListItem button>
                        <ListItemIcon >
                            <PersonIcon />
                        </ListItemIcon>
                        <ListItemText primary={"Profile"} />
                    </ListItem>
                </Link>

                <Divider />
                <Link to="/create-community" style={{ textDecoration: 'none', color: "#101010" }} >
                    <ListItem button>
                        <ListItemIcon>
                            <PeopleIcon />
                        </ListItemIcon>
                        <ListItemText primary={"Create Community"} />
                    </ListItem>
                </Link>
                <Divider />
                
                    <ListItem button onClick={logout}>
                        <ListItemIcon>
                            <Logout />
                        </ListItemIcon>
                        <ListItemText primary={"Logout"} />
                    </ListItem>
            </List>
        </Drawer>
    );
}

export default SideBar;