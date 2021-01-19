import useFetch from "../utils/useFetch"
import Spinner from 'react-bootstrap/Spinner';
import Alert from 'react-bootstrap/Alert';
import Table from 'react-bootstrap/Table';
import { useState } from "react";
import CenteredModal from './CenteredModal';

export default function Users(props) {
    const {data: users, isPending, error} = useFetch("http://localhost:7050/users/"+ props.db)
    
    const [id,setId] = useState(null)
    const [modalShow,setModalShow] = useState(false)


    const startModal = (user_id) => {
      setId(user_id)
      setModalShow(true)
    }
    
    return (
        <>
            <div className="center-box">
                {isPending && <Spinner animation="border" />}
                {error &&  <Alert variant="danger">{error}</Alert>}
                {users && 
                    <Table style={{width: "85%", "margin-top": "2vh"}} striped bordered hover>
                    <thead className="table-header">
                      <tr>
                        <th>#</th>
                        <th>Name</th>
                        <th>Default Tablespace</th>
                        <th>Temporary Tablespace</th>
                      </tr>
                    </thead>
                    <tbody>
                        {users.map(user =>{
                            return(
                            <tr onClick={() => startModal(user.USER_ID)}>
                                <td> {user.USER_ID} </td>
                                <td> {user.USER_NAME} </td>
                                <td> {user.DEFAULT_TABLESPACE} </td>
                                <td> {user.TEMPORARY_TABLESPACE} </td>
                            </tr>
                            )
                        })}
                    </tbody>
                  </Table>
                }
            </div>
            {id!==null && <CenteredModal header="Privileges" show={modalShow} onHide={() => {setId(null);setModalShow(false)}} user_id={id}/>}

        </>
    )
  }