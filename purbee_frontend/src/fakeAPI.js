

export const FakeCommunities = [
    {
        name: "NBA",
        post_types: [
            {
                name: "Game Result",
                id: "game_result_1",
                fields: {
                    plainTextList: [
                        {
                            header: "Team 1",
                            text: ""
                        },
                        {
                            header: "Team 2",
                            text: ""
                        },
                        {
                            header: "Points Scored of Team 1",
                            text: ""
                        },
                        {
                            header: "Points Scored of Team 2",
                            text: ""
                        },
                    ],
                    photoList: [
                        {
                            header: "Game Photo",
                            image: "",
                            description: ""
                        }
                    ],
                    dateList: [
                        {
                            header: "Game Date and Time",
                            date: "",
                            time: ""
                        }
                    ],
                    selectionList: [],
                    documentList: [],
                    eventList: [],
                    pollsList:[],
                    pricesList: [],
                    locationList: [
                        {
                            header: "Game Location",
                            location: "",
                            description: ""
                        }
                    ],
                }, 
                likeEnabled: true,
                communityEnabled: true,
                communityId: "NBA"
            },
            {
                name: "Next Game",
                id: "Next Game 1",
                fields: {
                    plainTextList: [
                        {
                            header: "Team 1",
                            text: ""
                        },
                        {
                            header: "Team 2",
                            text: ""
                        },
                    ],
                    photoList: [
                        {
                            header: "Game Photo",
                            image: "",
                            description: ""
                        }
                    ],
                    dateList: [
                        {
                            header: "Game Date and Time",
                            date: "",
                            time: ""
                        }
                    ],
                    selectionList: [],
                    documentList: [],
                    eventList: [],
                    pricesList: [],
                    pollsList: [
                        {
                            header: "Which Team Will Win?",
                            multiplte: false,
                            options: ["Team 1", "Team 2"],
                            values: [],
                        }
                    ],
                    locationList: [
                        {
                            header: "Game Location",
                            location: "",
                            description: ""
                        }
                    ],
                }, 
                likeEnabled: true,
                communityEnabled: true,
                communityId: "NBA"
            },
        ]
    },
    {
        name: "Cinema Enthusiasts",
        post_types: [
            {
                name: "Upcoming Movies",
                id: "upcoming_movies",
                fields: {
                    plainTextList: [
                        {
                            header: "Movie Name",
                            text: ""
                        },
                        {
                            header: "Starring",
                            text: ""
                        },
                        {
                            header: "Director",
                            text: ""
                        },
                    ],
                    photoList: [
                        {
                            header: "Photo",
                            image: "",
                            description: ""
                        }
                    ],
                    dateList: [
                        {
                            header: "Release Date",
                            date: "",
                            time: ""
                        }
                    ],
                    selectionList: [],
                    documentList: [],
                    eventList: [],
                    pricesList: [],
                    locationList: [],
                    pollsList:[],
                    likeEnabled: true,
                    communityEnabled: true,
                    communityId: "cinema_enthusiasts"
                }, 
            },
        ]    
    },
]