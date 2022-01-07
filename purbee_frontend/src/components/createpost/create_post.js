import {
    Box,
    Button,
    Grid,
    Link,
    MenuItem,
    Select,
    Typography,
    TextField,
    Divider,
} from '@material-ui/core';
import { useEffect, useState } from "react"
import Axios from 'axios'
import PostFields from './post_fields';
import { base_url, headers } from "../../utils/url"
import { getUser, setUserSession } from "../../utils/common"
import { useParams, useNavigate } from 'react-router-dom'


const CreatePost = () => {

    let navigate = useNavigate()

    const { community_id } = useParams()

    const [selectedCommunity, setSelectedCommunity] = useState();
    const [selectedPostType, setSelectedPostType] = useState();
    const [postTypes, setPostTypes] = useState([]);
    const [fields, setFields] = useState();
    const [postTitle, setPostTitle] = useState();
    


    useEffect(() => {
        async function funct() {
            let arr = []
            let postTypeIds = []
            let modelCommunity = {
                name: community_id,
                post_types: []
            };
            await Axios({
                headers: headers,
                method: "GET",
                url: base_url + 'community_page/' + community_id
            }).then(async response => {
                const community = response.data.community_instance;
                postTypeIds = community.post_type_id_list;
            }).then(async () => {
                await Promise.all(postTypeIds.map(async postTypeId => {
                    let request_json = {
                        "post_type_id": postTypeId
                    };
                    await Axios({
                        headers: headers,
                        method: "PUT",
                        url: base_url + 'post_type/',
                        data: request_json
                    }).then(async response => {
                        let postType = response.data.data;
                        let newPostType = {
                            name: postType.post_type_name,
                            id: postTypeId,
                            fields: {
                                plainTextList: [],
                                photoList: [],
                                dateList: [],
                                selectionList: [],
                                documentList: [],
                                eventList: [],
                                pollsList: [],
                                pricesList: [],
                                locationList: [],
                            },
                        }
                        postType.post_field_info_dictionaries_list.map(postField => {
                            if (postField.field_type == 'PlainText') { newPostType.fields.plainTextList.push({ header: postField.header, text: "" }) }
                            else if (postField.field_type == 'Photo') { newPostType.fields.photoList.push({ header: postField.header, image: "", description: "" }) }
                            // else if (postField.field_type == 'Selection') { newPostType.fields.pollsList.push({ header: postField.header, text: "" }) }
                            else if (postField.field_type == 'Document') { newPostType.fields.documentList.push({ header: postField.header, url: "", name: "" }) }
                            else if (postField.field_type == 'DateTime') { newPostType.fields.dateList.push({ header: postField.header, date: "", time: "" }) }
                            else if (postField.field_type == 'Location') { newPostType.fields.locationList.push({ header: postField.header, location: "", description: "" }) }
                            else if (postField.field_type == 'Price') { newPostType.fields.pricesList.push({ header: postField.header, location: "", description: "" }) }
                        })
                        modelCommunity.post_types.push(newPostType)
                        arr.push(newPostType)
                    }).then(_ => {
                        setPostTypes(arr)
                    }).catch(error => {
                        alert(error)
                    })
                }));
            })

            setSelectedCommunity(modelCommunity)
        }

        funct();
    }, [])

    const handleChangeOnPostTitle = (newPostTitle) => {
        setPostTitle(newPostTitle)
    }

    const handleSubmit = () => {
        console.log(selectedPostType.fields)
        const post = {
            post_type_id: selectedPostType.id,
            post_owner_user_name: getUser(),
            post_entries_dictionary_list: []
        }

        selectedPostType.fields.dateList.map((x, index) => {
            post.post_entries_dictionary_list.push({ header: x.header, date: fields.dates[index].toISOString().substring(0,10), time: fields.dates[index].toISOString().substring(11,19) })
        })

        selectedPostType.fields.documentList.map((docUrl, index) => {
            post.post_entries_dictionary_list.push({ header: fields.docNames[index], url: fields.docUrls[index] })
        })

        if (fields.location) {
            let loc = selectedPostType.fields.locationList[0]
            post.post_entries_dictionary_list.push({ header: loc.header, latitude: fields.location.lat, longitude: fields.location.lng, text: "" })
        }

        selectedPostType.fields.photoList.map((x, index) => {
            post.post_entries_dictionary_list.push({ header: fields.photoDescs[index], image: fields.photoUrls[index] })
        })

        selectedPostType.fields.plainTextList.map((x, index) => {
            post.post_entries_dictionary_list.push({ header: x.header, text: fields.plainTexts[index] })
        })
        // selectedPostType.fields.pollsList.map((x, index) => {
        //     post.post_entries_dictionary_list.push({ header: x.header, options: fields.pollOptions })
        // })

        selectedPostType.fields.pricesList.map((x, index) => {
            post.post_entries_dictionary_list.push({ header: x.header, amount: fields.prices[index], currency: 'usd' })
        });

        post.post_title = postTitle
        let request_json = post;
        Axios({
            headers: headers,
            method: "POST",
            url: base_url + 'post/',
            data: request_json
        }).then(() => {
            alert("Post Created")
            navigate('/community-home/' + community_id)
        }).catch(error => {
            console.log(error)
            alert(error)
        })
    };

    if (!postTypes.length) {
        return (
            <div> Loading... </div>
        )
    } else {

        return (
            <div style={{ display: "flex", justifyContent: "center", alignItems: "center", paddingTop: "60px", paddingBottom: "100px" }}>
                
                <form style={{ backgroundColor: "#fff", width: "36%", padding: "20px", borderRadius: "4%" }} onSubmit={handleSubmit}>
                <Typography
                                color="textPrimary"
                                sx={{ mb: 1 }}
                                variant="subtitle2"
                                align='left'
                            >
                                Post Title
                            </Typography>
                    <TextField onChange={(e) => { handleChangeOnPostTitle(e.target.value) }} variant="outlined" fullWidth />
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
                                Post Type
                            </Typography>
                            <Select
                                fullWidth
                                name="title"
                                variant="outlined"
                                align="left"
                                value={selectedPostType}
                            >
                                {postTypes.map((post_type) => (
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
                            <PostFields community={selectedCommunity} post_type={selectedPostType} setFields={setFields} />
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
                            onClick={handleSubmit}
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
    }

};

export default CreatePost;
