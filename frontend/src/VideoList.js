import Video from "./Video";

export default function VideoList() {

    let items = [
        {"title": "Test Title", "name": "Test Author", "link": "hgttbtl", "tags": ["1", "2", "3"], "description": "description1"},
        {"title": "Test Title1", "name": "Test Author1", "link": "hgttbtl1111", "tags": ["11", "21", "31"], "description": "description2"},
        {"title": "Test Titl2", "name": "Test Author2", "link": "hgttbtl3353", "tags": ["11", "2", "31"], "description": "description3"},
    ]
    const listItems = items.map(video => <Video{...video}/>);
    return (
    <ul>
        {listItems}
    </ul>
);
}
