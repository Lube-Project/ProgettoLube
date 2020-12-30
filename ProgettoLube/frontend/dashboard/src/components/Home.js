import React, { useState, useEffect } from 'react';
import { Link, useHistory } from 'react-router-dom';
import '../css/App.css';
import Button from "@material-ui/core/Button";
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import {
  DataGrid,
  ColDef,
  ValueGetterParams,
  CellParams,
  GridApi
} from "@material-ui/data-grid";

function Home() {

  // viene eseguito appena viene caricata la pagina
  useEffect(() => {
    fetchData();
  }, []);

  const [posts, setPosts] = useState([]);
  
  const history = useHistory();

  // chiamata fake per richiedere i dati 
  const fetchData = async () => {
    const rawData = await fetch('https://jsonplaceholder.typicode.com/posts');

    // adesso trasformo i dati ricevuti in json
    const data = await rawData.json();

    const posts = data.slice(0, 10);    // con slice prendiamo solo i primi 10 elementi dell'array
    console.log(posts);

    setPosts(posts);
  }

  const columns = [
    {
      field: "",
      headerName: "Button",
      sortable: false,
      width: 100,
      disableClickEventBubbling: true,
      renderCell: (params: CellParams) => {
        const onClick = () => {
          const api: GridApi = params.api;
          const fields = api
            .getAllColumns()
            .map((c) => c.field)
            .filter((c) => c !== "__check__" && !!c);
          const thisRow = {};

          fields.forEach((f) => {
            thisRow[f] = params.getValue(f);
          });

          let path = `/${thisRow.id}`;
          return history.push(path);
        };

        return <Button onClick={onClick}>Dettagli</Button>;
      }
    },
    { field: 'userId', headerName: 'Nome', width: 200 },
    { field: 'id', headerName: 'Data', width: 200 },
    { field: 'title', headerName: 'Correttezza', width: 200 },
    { field: 'body', headerName: 'Dettagli', width: '100%' },
  ];

  return (
    <div className="App">
      <h1>HOME</h1>

      <h2>Carosello</h2>
      <h2>SITI | SOCIAL</h2>

      <div className="ContainerTabella">
        <div className="Tabella">
          <DataGrid rows={posts} columns={columns} />
        </div>
      </div>

      {/* posts.map(post => (
        <Link key={post.id} to={`/${post.id}`}>
          <h4 key={post.id} >{post.title}</h4>
        </Link>
      )) */}
    </div>
  );
}

export default Home;
