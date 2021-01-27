import {useParams} from "react-router-dom";
import Navbar from "./Navbar";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import StorageStats from "./StorageStats";
import SystemStats from "./SystemStats";
import UsersStats from "./UsersStats";

export default function(props){
    const params = useParams()



    return (
        <>
            <Switch>
                <Route path={`${props.path}/:db_name/system`}>
                    <Navbar selectedDB={params.db_name} selected={1} showLinks={true} path={props.path + "/" + params.db_name}/>
                    <SystemStats db={params.db_name}/>
                </Route>
                <Route path={`${props.path}/:db_name/storage`}>
                    <Navbar selectedDB={params.db_name} selected={2} showLinks={true} path={props.path + "/" + params.db_name}/>
                    <StorageStats db={params.db_name}/>                    
                </Route>    
                <Route path={`${props.path}/:db_name/users`}>
                    <Navbar selectedDB={params.db_name} selected={3} showLinks={true} path={props.path + "/" + params.db_name}/>
                    <UsersStats db={params.db_name}/>
                </Route>
            </Switch>
        </>
    )
}