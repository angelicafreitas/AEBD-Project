import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from './components/Navbar'
import DBSelector from './components/DBSelector'
import Monitor from './components/Monitor'
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";
import { AnimateOnChange } from 'react-animation'


function App() {
  return (
    <div className="App">
      <Router>
          <Switch>
            <Route exact path="/">
              <DBSelector />
            </Route>
            <Route path="/monitor/:db_name">
              <Monitor path="/monitor"/>
            </Route>
            <Route>
              ERROR 404
            </Route>
          </Switch>
        
      </Router>
    </div>
  );
}

export default App;
