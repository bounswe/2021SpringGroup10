import {
    Box,
    Button,
    Grid,
    Typography,
    Switch,
    TextField,
} from '@material-ui/core';
import { useEffect, useState } from "react"

export const CreateCommunity = () => {
    const [communityId, setCommunityId] = useState("");
    const [isPrivate, setPrivate] = useState(false);
    const [description, setDescription] = useState("");
    const [photo, setPhoto] = useState("https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg");

    const handleSubmit = () => {

    }

    const handleCommunityIdChange = (newId) => {
        setCommunityId(newId);
    }

    const handlePhotoChange = (newPhoto) => {
        setPhoto(newPhoto)
    }

    const handleDescriptionChange = (newDescription) => {
        setDescription(newDescription);
    }

    return (
        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", paddingTop: "60px", paddingBottom: "100px" }}>
            <form style={{ backgroundColor: "#fff", width: "36%", padding: "20px", borderRadius: "4%" }} onSubmit={handleSubmit} >
                <Grid container>
                    <Grid container>
                        
                        <Grid
                            item
                            xs={6}
                            sm={6}
                        >
                            <img src={photo} style={{ width: "50%", alignSelf: "center" }}></img>
                        </Grid>
                        <Grid
                            item
                            xs={6}
                            sm={6}
                        >
                            <Typography
                                color="textPrimary"
                                sx={{ mb: 1 }}
                                variant="subtitle1"
                            >
                                Community Profile Photo
                            </Typography>
                            <TextField helperText={"Photo URL"} onChange={(e) => { handlePhotoChange(e.target.value) }} variant="outlined" fullWidth />
                            <div style={{ height: "1em" }}></div>
                            <Typography
                                color="textPrimary"
                                sx={{ mb: 1 }}
                                variant="subtitle1"
                            >
                                Private
                            </Typography>
                            <Switch checked={isPrivate} onChange={(e) => { setPrivate(e.target.checked) }} color="primary" />
                        </Grid>
                    </Grid>
                    <Grid
                        item
                        xs={12}
                        sm={12}
                    >
                        <div style={{ height: "3em" }}></div>
                        <Typography
                            color="textPrimary"
                            sx={{ mb: 1 }}

                            align='left'
                        >
                            Community Id
                        </Typography>
                        <TextField onChange={(e) => { handleCommunityIdChange(e.target.value) }} variant="outlined" fullWidth />
                        <div style={{ height: "2em" }}></div>
                    </Grid>
                    <Grid
                        item
                        xs={12}
                        sm={12}
                    >
                        <Typography
                            color="textPrimary"
                            sx={{ mb: 1 }}
                            align='left'
                        >
                            Community Manifest
                        </Typography>
                        <TextField multiline={true} minRows={5} onChange={(e) => { handleDescriptionChange(e.target.value) }} variant="outlined" fullWidth />
                    </Grid>
                    <div style={{ height: "7em" }}></div>
                    <Grid
                        item
                        xs={4}
                        sm={4}
                    >
                        <Box
                            sx={{
                                display: 'flex',
                                justifyContent: 'center',
                                mt: 3
                            }}
                        >
                            <Button
                                color="primary"
                                fullWidth
                                size="medium"
                                variant="contained"
                                onClick={handleSubmit}
                                disabled={!communityId}
                            >
                                Create Your Community!
                            </Button>
                        </Box>

                    </Grid>
                    <Grid
                        item
                        xs={7}
                        sm={7}
                    >
                        <div style={{ height: "2em" }}></div>
                        <Typography
                            color="textSecondary"
                            sx={{ mb: 1 }}
                            align='right'
                        >
                            You can change other details about your community in community page.
                        </Typography>
                    </Grid>
                </Grid>
            </form>
        </div>
    )

}

export default CreateCommunity;