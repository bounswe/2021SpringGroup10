import {
    Box,
    Button,
    Grid,
    Link,
    MenuItem,
    Select,
    Typography,
    Divider,
    Switch,
    IconButton,
    TextField,
} from '@material-ui/core';
import { useEffect, useState } from "react"
import { FakeCommunities } from '../../fakeAPI';
import AddBoxIcon from '@mui/icons-material/AddBox';


export const CreatePostType = () => {
    const data = FakeCommunities;

    const [selectedCommunity, setSelectedCommunity] = useState();
    const [fields, setFields] = useState([]);
    const [refresh, setRefresh] = useState(false);
    const [label, setLabel] = useState("");
    const [comments, setComments] = useState(false);
    const [like, setLike] = useState(false);
    const postFieldsList = ["Plain Text", "Photo", "Date", "Selection", "Document", "Price", "Location"];
    const emptyField = { type: "", label: "" };



    const handleAddField = () => {
        let arr = fields;
        arr.push(emptyField);
        setFields(arr);
    }

    const handleTypeSelect = (type, index) => {
        if (type != "Select") {
            let arr = fields;
            arr[index].type = type;
            setFields(arr)
        }
    }


    const handleChangeLabel = () => {
        let lab = label;
        const words = label.split(" ");
        const index = words[words.length - 1];
        let arr = fields;
        if(arr[index]) {
            arr[index].label = lab.replace(index, "").trim();
            setFields(arr);
        }
    }

    const handleSubmit = () => {
        let x = false
        fields.map(field => {
            if(!field.type || !field.label){
                x = true;
            }
        })
        if(selectedCommunity && !x){
            alert("Post Type Created!");     
        } else {
            alert("Smthng wrong!")
        }
    }

    useEffect(() => {
        handleChangeLabel()
        setRefresh(!refresh);
     }, [label]);



    return (
        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", paddingTop: "60px", paddingBottom: "100px" }}>
            <form style={{ backgroundColor: "#fff", width: "36%", padding: "20px", borderRadius: "4%" }} onSubmit={handleSubmit} >
                <Grid
                    container
                    spacing={3}
                >
                    <Grid
                        item
                        xs={12}
                        sm={12}
                    >
                        <Typography
                            color="textPrimary"
                            sx={{ mb: 1 }}
                            variant="subtitle2"
                            align='left'
                        >
                            Community
                        </Typography>
                        <Select
                            fullWidth
                            name="title"
                            variant="outlined"
                            value={selectedCommunity}
                            align="left"
                        >
                            {data.map((community) => (
                                <MenuItem value={community} onClick={() => { setSelectedCommunity(community); setFields([]) }}>{community.name}</MenuItem>
                            ))}
                        </Select>
                    </Grid>

                    <Grid
                        item
                        xs={4}
                        sm={4}
                    >
                        <Typography
                            color="textPrimary"
                            sx={{ mb: 1 }}
                            disabled={!selectedCommunity}
                            variant="subtitle1"
                        >
                            Likeable
                        </Typography>
                        <Switch checked={like} onChange={(e) => {setLike(e.target.checked)}} color="primary" />
                    </Grid>

                    <Grid
                        item
                        xs={4}
                        sm={4}
                    >
                        <Typography
                            color="textPrimary"
                            sx={{ mb: 1 }}
                            variant="subtitle1"
                            disabled={!selectedCommunity}
                        >
                            Comments
                        </Typography>
                        <Switch checked={comments} onChange={(e) => {setComments(e.target.checked)}} color="primary" />
                    </Grid>

                    <Grid
                        item
                        xs={4}
                        sm={4}
                    >
                        <Typography
                            color="textPrimary"
                            sx={{ mb: 1 }}
                            variant="subtitle1"
                        >
                            Add Field
                        </Typography>
                        <IconButton color="primary" onClick={() => { handleAddField(); setRefresh(!refresh) }}><AddBoxIcon /></IconButton>
                    </Grid>

                    {fields.map((_, index) => (
                        <Grid container spacing={3}>
                            <Grid item xs={6} sm={6}>
                                <Typography
                                    color="textPrimary"
                                    sx={{ mb: 1 }}
                                    variant="subtitle2"
                                    align='left'
                                >
                                    Type
                                </Typography>
                                <Select fullWidth error={!fields[index].type} color="primary" variant='outlined' defaultValue={"Select"} labelId={"as" + index} disabled={!selectedCommunity} >
                                    <MenuItem value="Select" disabled>Select</MenuItem>
                                    {postFieldsList.map(postField => (
                                        <MenuItem  value={postField} onClick={() => { handleTypeSelect(postField, index); setRefresh(!refresh) }}>{postField}</MenuItem>
                                    ))}
                                </Select>
                            </Grid>
                            <Grid item xs={6} sm={6}>
                                <Typography
                                    color="textPrimary"
                                    sx={{ mb: 1 }}
                                    variant="subtitle2"
                                    align='left'
                                >
                                    Label
                                </Typography>
                                <TextField error={!fields[index].label} variant="outlined" fullWidth onChange={(e) => { setLabel(e.target.value + " " + index) }}></TextField>
                            </Grid>
                            <Grid item sm={12} xs={12}>
                                <Divider padding="4px" />
                            </Grid>
                        </Grid>
                    ))}

                </Grid>
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
                        size="large"
                        variant="contained"
                        onClick={handleSubmit}
                        disabled={!selectedCommunity || !fields.length}
                    >
                        Create Post Type!
                    </Button>
                </Box>
                <Typography
                    color="textSecondary"
                    sx={{ mt: 3 }}
                    variant="body2"
                >
                    By creating this, you agree to the
                    {' '}
                    <Link
                        color="textPrimary"
                        href="#"
                        underline="always"
                        variant="subtitle2"
                    >
                        Privacy Policy
                    </Link>
                    {' '}
                    and
                    {' '}
                    <Link
                        color="textPrimary"
                        href="#"
                        underline="always"
                        variant="subtitle2"
                    >
                        Cookie Policy
                    </Link>
                    .
                </Typography>
            </form>
        </div>

    );

};

export default CreatePostType;
