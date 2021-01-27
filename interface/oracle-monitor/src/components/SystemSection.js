import useFetch from '../utils/useFetch';
import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import { useState } from 'react';



export default function SystemSection(props) {

    const {data, isPending, error} = useFetch(props.url)
    const [close, setClose] = useState(true)


    return (
    <div className="section">
      
      <div onClick={() => setClose(!close)} className="sectionHeader">
          <h5>{props.title}</h5>
          <small>{props.subtitle}</small>
      </div>
      <div className={!close ? "section-content" : "section-content fade"}>
        {!close && isPending && <Spinner animation="border" />}
        {error &&  <Alert variant="danger">{error}</Alert>}
        {!close && data && props.transform(data) }
      </div>
    
    </div>)
  }