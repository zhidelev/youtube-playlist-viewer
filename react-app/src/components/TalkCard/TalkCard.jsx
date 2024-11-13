function TalkCard({ props }) {

    const list_name = props.list;
    const is_processed = props.processed

    return (
        <p>{list_name}</p>)
};

export default TalkCard;