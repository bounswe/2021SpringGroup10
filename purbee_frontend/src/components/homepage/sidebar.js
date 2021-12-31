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
import NotificationsIcon from '@mui/icons-material/Notifications';
import { purple } from '@mui/material/colors';

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
                <Link to="/profile-page" style={{ textDecoration: 'none', color: "#101010" }} >
                    <ListItem button >
                        <ListItemIcon >
                            <HomeIcon />
                        </ListItemIcon>
                        <ListItemText primary={"Home"} />
                    </ListItem>
                </Link>
                <Divider />

                <Link to="/profile-page" style={{ textDecoration: 'none', color: "#101010" }} >
                    <ListItem button>
                        <ListItemIcon >
                            <PersonIcon />
                        </ListItemIcon>
                        <ListItemText primary={"Profile"} />
                    </ListItem>
                </Link>

                <Divider />
                <Link to="/about" style={{ textDecoration: 'none', color: "#101010" }} >
                    <ListItem button>
                        <ListItemIcon>
                            <NotificationsIcon />
                        </ListItemIcon>
                        <ListItemText primary={"Notifications"} />
                    </ListItem>
                </Link>
            </List>
        </Drawer>
    );
}

export default SideBar;