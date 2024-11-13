import "./ConfVideoList.css";
import ConfCard from '../ConfCard/ConfCard';
import { useEffect, useState } from 'react';

function ConfVideoList() {
    const [items, setItems] = useState([]);

    useEffect(() => {
        fetch('http://localhost:8000/lists').then(response => {
            return response.json();
        }).then((data) => {
        setItems(data)}); // Update data state;
    }, [items])

    return (
        <div>
        <h1>ConfVideoList</h1>
        <table>
            <thead>
                <tr>
                    <td>Conference</td>
                    <td>Processed</td>
                </tr>
            </thead>
            <tbody>
            {items.map((item, index) => (
                <ConfCard key={index} item={item} index={index} props={item} />
                ))}
            </tbody>
            <tfoot></tfoot>
        
        </table>
        </div>
    );
}

export default ConfVideoList;