import React, { Component } from 'react';
import Header from '../main/Header';
import {API_ROOT_URL} from '../../constants';

class SnapshotPage extends Component {
    state = {data: null};
    user_id = this.props.match.params.user_id;
    timestamp = this.props.match.params.timestamp;

    render() {
    return (
      <div className="App">
        <Header title={"Snapshot by User #"+this.user_id} />
        howdy :^]


      </div>
    );
    }

}

export default SnapshotPage;