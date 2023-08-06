function Video(props) {
    let link = props.link;
    let name = props.name;
    let description = props.description;
    return (
    <div className="container mx-auto m-4 bg-sky-100 px-10 hover:bg-sky-200 font-sans rounded-lg ring-2 ring-blue-500">
        <a href={link}>{name}</a>
        Texxt
        <p className="text-lg">
            {description}
        </p>
        <p>
            {props.tags}
        </p>
    </div>
    );
  }

export default Video;