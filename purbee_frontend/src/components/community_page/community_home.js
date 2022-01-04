import React from "react";
import { MockCommunity } from './mockCommunity'
import './community_home.css'

export const CommunityHome2 = () => {
    const [member_count, set_member_count] = React.useState("");
    const join_community = (event) => {
        console.log(data.member_count);
        set_member_count(member_count + 1);
    }
    const data = MockCommunity;
    React.useEffect(() => {
        set_member_count(data.member_count);
    },[])

    return (
        <section className="section about-section gray-bg" id="about">
            <div className="container">
                <div className="row align-items-center flex-row-reverse">
                    <div className="col-lg-6">
                        <div className="about-text go-to">
                            <h3 className="dark-color">{data.name}</h3>
                            <p> {data.description} </p>
                            <div className="row about-list">
                                <div className="col-md-6">
                                    <div className="media">
                                        <label style={{width: "120px"}}> Creation Date </label>
                                        <p>{data.creation_date}</p>
                                    </div>
                                    <div className="media">
                                        <label> Creator </label>
                                        <p> { data.creator } </p>
                                    </div>
                                    <div className="media">
                                        <label>Location</label>
                                        <p>{data.location}</p>
                                    </div>
                                    <div className="media">
                                        <label style={{width: "100px"}}>Post Types</label>
                                        {data.post_types.map(pt => <div> {pt} </div>)}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-lg-6">
                        <div className="about-avatar">
                            <img src="https://imgur.com/yCWExHi.png" title="Community Picture" alt=""/>
                        </div>
                    </div>
                </div>
                <div className="counter">
                    <div className="row">
                        <div className="col-6 col-lg-3">
                            <div className="count-data text-center">
                                <h6 className="count h2">{member_count}</h6>
                                <p className="m-0px font-w-600">Member Count</p>
                            </div>
                        </div>
                        <div className="col-6 col-lg-3">
                            <div className="count-data text-center">
                                <h6 className="count h2" data-to={data.post_count} data-speed={data.post_count}>{data.post_count}</h6>
                                <p className="m-0px font-w-600">Post Count</p>
                            </div>
                        </div>
                        <div className="col-6 col-lg-3">
                            <div className="count-data text-center">
                                <button type="button" className="btn btn-primary" onClick={join_community}> Join! </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default CommunityHome2;