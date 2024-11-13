import "./SubmitForm.css";
import Button from '../Button/Button';

function SubmitForm() {
    const handleClick = (e) => {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        const formJson = Object.fromEntries(formData.entries());
        console.log(formJson);

        fetch('http://localhost:8000/data', {
            method: form.method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formJson),
        })
        .then(response => {
            console.log(response.json());
            console.log(response.status);
        });


    }
    return (
        <form method="post" onSubmit={handleClick}>
            <p>Please input conference playlist:</p>
            <input className="url_input" type="text" id="playlist" name="url"/>
            <Button />
        </form>
        
    );
}

export default SubmitForm;