import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../css/App.css';

function Post(props) {

    // viene eseguito appena viene caricata la pagina
    useEffect(() => {
        fetchData();
    }, []);

    const [post, setPost] = useState({});

    // chiamata fake per richiedere i dati 
    const fetchData = async () => {
        const id = props.match.params.id;
        const rawData = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`);
        const post = await rawData.json();

        console.log(post);

        setPost(post);
    }

    return (
        <div className="App">

            <h1>{post.title}</h1>
            <h3>{post.body}</h3>

        </div>
    );
}

export default Post;
