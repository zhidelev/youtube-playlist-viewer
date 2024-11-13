function ConfCard({ props }) {

    const list_name = props.list;
    const is_processed = props.processed;

    return (
        <tr>
            <td>{list_name}</td>
            <td>{is_processed? "True" : "False"}</td>
        </tr>)
};

export default ConfCard;