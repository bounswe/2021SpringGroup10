import {
    Box,
    Button,
    Grid,
    Link,
    MenuItem,
    Select,
    Typography,
    Divider,
} from '@material-ui/core';
import { useState } from "react"
import { FakeCommunities } from '../../fakeAPI';
import PostFields from './post_fields';

const CreatePost = () => {
    const handleSubmit = (event) => {
        event.preventDefault();
    };


    const data = FakeCommunities;

    console.log(data);

    const [selectedCommunity, setSelectedCommunity] = useState();
    const [selectedPostType, setSelectedPostType] = useState();

    return (
        <div style={{display: "flex", justifyContent: "center", alignItems: "center", paddingTop: "60px", paddingBottom: "100px" }}>
            <form style={{ backgroundColor: "#fff", width: "36%", padding: "20px", borderRadius: "4%" }} onSubmit={handleSubmit}>
                <Grid
                    container
                    spacing={3}
                >
                    <Grid
                        item
                        xs={6}
                        sm={6}
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
                                <MenuItem value={community} onClick={() => { setSelectedCommunity(community) }}>{community.name}</MenuItem>
                            ))}
                        </Select>
                    </Grid>
                    <Grid
                        item
                        xs={6}
                        sm={6}
                    >
                        <Typography
                            color="textPrimary"
                            sx={{ mb: 1 }}
                            variant="subtitle2"
                            align='left'
                        >
                            Post Type
                        </Typography>
                        <Select
                            fullWidth
                            name="title"
                            variant="outlined"
                            align="left"
                            disabled={!selectedCommunity}
                            value={selectedPostType}
                        >
                            {selectedCommunity?.post_types?.map((post_type) => (
                                <MenuItem value={post_type} onClick={() => { setSelectedPostType(post_type) }}>{post_type.name}</MenuItem>
                            ))}
                        </Select>
                    </Grid>
                    <Grid
                        item
                        xs={12}
                        sm={12}
                    >
                        <Divider />
                        <PostFields community={selectedCommunity} post_type={selectedPostType} />
                    </Grid>
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
                    >
                        Let&apos;s Share!
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

export default CreatePost;
