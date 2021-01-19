import useFetch from "../utils/useFetch"
import Navbar from "./Navbar"

import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

export default function(props){
    const {data : dbs, isPending, error} = useFetch("http://localhost:7050/db")
    return(
        <>
            <Navbar showLinks={false}/>
            <div className="center-box">
                <h1 style={{"self-align" : "center"}} className="display-3">Welcome!</h1>
                {isPending && <Spinner animation="border" />}
                {error &&  <Alert variant="danger">{error}</Alert>}
                {dbs && dbs.map(el => {
                    return(<Card style={{ width: 'auto', "margin-top": "2vh" }}>
                    <Card.Body>
                      <Card.Title>{el.DATABASE_NAME}</Card.Title>
                      <Card.Subtitle className="mb-2 text-muted">{el.INSTANCE_NAME}</Card.Subtitle>
                      <Card.Text>
                        <span>
                            <span>{el.VERSION}</span>
                        </span>
                      </Card.Text>
                      <Button as="a" href={"/monitor/" + el.DATABASE_NAME + "/system"} size="sm" variant="outline-dark">Select</Button>
                    </Card.Body>
                  </Card>)
                })}
            </div>
            
        </>
    )
}