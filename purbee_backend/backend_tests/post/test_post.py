import pytest
import requests

base_url = "http://3.134.93.99:8080/api"

mock_post_type_id = None
mock_post_id = None


@pytest.mark.dependency(name="test_create_post_type", depends=[])
def test_create_post_type():
    global mock_post_type_id
    mock_create_post_type_request = {
    "post_type_name": "Mock Post Type",
    "parent_community_id": "10",
    "post_field_info_dictionaries_list": [
        {
            "header": "Event Description",
            "field_type": "PlainText"
        },
        {
            "header": "Event Cost",
            "field_type": "Price"
        },
        {
            "header": "Event Location",
            "field_type": "Location"
        },
        {
            "header": "Event Participation",
            "field_type": "Participation"
        },
        {
            "header": "Event Poll",
            "field_type": "Poll"
        },
        {
            "header": "Event Document",
            "field_type": "Document"
        },
        {
            "header": "Event DateTime",
            "field_type": "DateTime"
        },
        {
            "header": "Event Photo",
            "field_type": "Photo"
        }
    ]
}
    url = base_url + "/post_type/"
    res = requests.post(url, json=mock_create_post_type_request).json()
    assert (res.get("response_message") == "PostType is successfully created.")

    if res.get("response_message") == "PostType is successfully created.":
        mock_post_type_id = res["data"]["_id"]


@pytest.mark.dependency(name="test_get_post_type", depends=["test_create_post_type"])
def test_get_post_type():
    url = base_url + "/post_type/"
    res = requests.put(url, json={"post_type_id": mock_post_type_id}).json()
    assert (res.get("response_message") == "PostType is successfully retrieved.")


@pytest.mark.dependency(name="test_create_post", depends=["test_get_post_type"])
def test_create_post():
    global mock_post_id
    mock_create_post_request = {
        "post_type_id": mock_post_type_id,
        "post_title": "Example Post Title",
        "post_owner_user_name": "eking",
        "post_entries_dictionary_list": [
            {
                "header": "Event Description",
                "text": "The torunament will host The top 100 ATP players."
            },
            {
                "header": "Event Cost",
                "amount": 17,
                "currency": "tl"
            },
            {
                "header": "Event Location",
                "latitude": 38.8951,
                "longitude": -77.0364,
                "text": "Court number 4."
            },
            {
                "header": "Event Participation"
            },
            {
                "header": "Event Poll",
                "options": [
                    "Option A",
                    "Option B",
                    "Option C",
                    "Option D"
                ],
                "can_vote_for_n_many_options": 2
            },
            {
                "header": "Event Document",
                "url": "some_url"
            },
            {
                "header": "Event Photo",
                "image": "image_link"
            },
            {
                "header": "Event DateTime",
                "date": "23/03/2021",
                "time": "12:33"
            }
        ]
    }
    url = base_url + "/post/"
    res = requests.post(url, json=mock_create_post_request).json()
    assert (res.get("response_message") == "Post is successfully created. ")

    if res.get("response_message") == "Post is successfully created. ":
        mock_post_id = res["data"]["_id"]


@pytest.mark.dependency(name="test_get_post", depends=["test_create_post"])
def test_get_post():
    url = base_url + "/post/"
    res = requests.put(url, json={"post_id": mock_post_id}).json()
    resp_message = res.get("response_message")
    assert (resp_message == "Post is successfully returned. ")


@pytest.mark.dependency(name="test_like_post", depends=["test_get_post"])
def test_like_post():
    mock_like_post_request = {
        "post_id": mock_post_id,
        "user_name": "liker"
    }
    url = base_url + "/post/like/"
    res = requests.put(url, json=mock_like_post_request).json()
    assert ("successfully" in res.get("response_message"))


@pytest.mark.dependency(name="test_unlike_post", depends=["test_get_post"])
def test_unlike_post():
    mock_unlike_post_request = {
        "post_id": mock_post_id,
        "user_name": "liker"
    }
    url = base_url + "/post/unlike/"
    res = requests.put(url, json=mock_unlike_post_request).json()
    assert ("successfully" in res.get("response_message"))


@pytest.mark.dependency(name="test_participate_in_post", depends=["test_get_post"])
def test_participate_in_post():
    mock_participate_request = {
        "post_id": mock_post_id,
        "user_name": "participator",
        "header_of_participation_field": "Event Participation"
    }
    url = base_url + "/post/participate/"
    res = requests.put(url, json=mock_participate_request).json()
    assert ("successfully" in res.get("response_message"))


@pytest.mark.dependency(name="test_cancel_participation_in_post", depends=["test_get_post"])
def test_cancel_participation_in_post():
    mock_cancel_participate_request = {
        "post_id": mock_post_id,
        "user_name": "participator",
        "header_of_participation_field": "Event Participation"
    }
    url = base_url + "/post/cancel_participation/"
    res = requests.put(url, json=mock_cancel_participate_request).json()
    assert ("successfully" in res.get("response_message"))


@pytest.mark.dependency(name="test_vote_in_post", depends=["test_get_post"])
def test_vote_in_post():
    mock_vote_request = {
        "post_id": mock_post_id,
        "voter_user_name": "voter",
        "header_of_poll_field": "Event Poll",
        "option": "Option D"
    }
    url = base_url + "/post/vote/"
    res = requests.put(url, json=mock_vote_request).json()
    assert ("successfully" in res.get("response_message"))


@pytest.mark.dependency(name="test_cancel_vote_in_post", depends=["test_get_post"])
def test_cancel_vote_in_post():
    mock_cancel_vote_request = {
        "post_id": mock_post_id,
        "voter_user_name": "voter",
        "header_of_poll_field": "Event Poll",
        "option": "Option D"
    }
    url = base_url + "/post/cancel_vote/"
    res = requests.put(url, json=mock_cancel_vote_request).json()
    assert ("successfully" in res.get("response_message"))
