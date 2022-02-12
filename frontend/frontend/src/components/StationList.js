import React from "react";
import axios from "axios";

import './StationList.css';

import { generateInfo } from "./api";

class StationList extends React.Component{
  constructor(props){
    super(props);

    this.state = {
      station: "",
      date_from: "",
      date_to: "",
      testok: null,
      error: null
    };

    this.handlestation = this.handlestation.bind(this);
    this.handledateto = this.handledateto.bind(this);
    this.handledatefrom = this.handledatefrom.bind(this);
  }

handlestation(e){
  const name = e.target.name;
  const value = e.target.value;
  this.setState({ [name]: value});
}

handlestationto(e){
  const name = e.target.name;
  const value = e.target.value;
  this.setState({ [name]: value});
}

handlestationfrom(e){
  const name = e.target.name;
  const value = e.target.value;
  this.setState({ [name]: value});
}


 handleRequest(e) {
    this.setState({ error: null });
    if (this.state.station && this.state.datefrom && this.state.dateto) {
      this.setState({ testok: null });
      let reqObj = {
        station: this.state.station,
        datefrom: this.state.date_from.from,
        dateto: this.state.dateto
      };
      generateInfo(reqObj)//return a json with info or null
        .then(json => {
          setTimeout(() => {
            this.setState( {testok: json.data.info} );
          }, 0);
        })
        .catch(err => {
          this.setState({ error: err.error })
        });
    } else {
      this.setState({ error: "Invalid parameters" });
    }
  }



render() {
  return(
      <div className="new-form">
          <h1> Passes Per station</h1>

          <input name="station"
             field="station"
             placeholder="station"
             value={this.state.station}
             onChange={this.handlestation}

              />

           <input name="datefrom"
            type="datefrom"
            field="datefrom"
            placeholder="datefrom"
            value={this.state.datefrom}
            onChange={this.handledatefrom}
            />

          <input name="dateto"
            type="dateto"
            field="dateto"
            placeholder="dateto"
            value={this.state.dateto}
            onChange={this.handledateto}
            />


            <button className="btn waves-effect waves-light submit-btn"
             name="action"
             onClick={this.handleRequest}
             >
             Ok
             </button>

            {this.state.error !== null && (
            <div className="error">
              {this.state.error}
            </div>
            )}

            {this.state.testok !== null &&(
            <div className="testok">
               Succesful!
               <a target="_new" href={this.state.testok}> {this.state.testok}</a>
               {this.handlewindow()}
            </div>
          )}
      </div>

    );

 }
}

export default StationList;