import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from './components/Navbar'
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import { AnimateOnChange } from 'react-animation'

function App() {
  return (
    <div className="App">
      <Router>
          <Switch>
            <Route exact path="/">
            <Navbar />
              Home
            </Route>
            <Route path="/system">
            <Navbar option="system"/>
              System
            </Route>
            <Route path="/storage">
            <Navbar option="storage"/>
              Storage
            </Route>
            <Route path="/users">
            <Navbar option="users"/>
              Users
            </Route>
            <Route>
            <Navbar />
              ERROR 404
            </Route>
          </Switch>
        
      </Router>
    </div>
  );
}

export default App;
