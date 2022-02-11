import React from "react";
import axios from "axios";

const path = 'http://localhost:8000/interoperability/api/';

export default class StationList extends React.Component {
  state = {
    stations: []
  };

  componentDidMount() {
    axios.get(path+ 'stations').then(res => {
      const stations = res.data;
      this.setState({ stations });
    });
  }

  render() {
    return (
      <select>
        {this.state.stations.map(station => <option>{station.name}</option>)}
      </select>
    );
  }
}