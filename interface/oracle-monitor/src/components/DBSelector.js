import useFetch from "../utils/useFetch"
import Navbar from "./Navbar"

import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';

export default function(props){
    const {data : dbs, isPending, error} = useFetch("http://localhost:7050/db")

    return(
        <>
            <Navbar showLinks={false}/>
            <div className="center-box">
                <h1 style={{"self-align" : "center"}} className="display-3">Welcome!</h1>
                {isPending && <Spinner animation="border" />}
                {error &&  <Alert variant="danger">{error}</Alert>}

            </div>
            
        </>
    )
}