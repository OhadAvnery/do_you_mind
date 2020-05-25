import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter as Router, Switch, 
    Route, Link} from "react-router-dom";

import App from './App';
import UsersPage from './components/users/UsersPage';
import UserPage from './components/user/UserPage';
import SnapshotPage from './components/snapshot/SnapshotPage';
import './index.css';

const router = 
(<Router>
      <div>
        
        <Switch>
            <Route exact path="/" component={App} />
            <Route exact path="/users" component={UsersPage} />
            <Route exact path="/users/:user_id" component={UserPage} />
            <Route exact path="/users/:user_id/:timestamp" component={SnapshotPage} />

        </Switch>
      </div>
</Router>)

ReactDOM.render(router, document.getElementById('root'));
