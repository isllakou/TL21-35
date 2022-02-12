import React from "react";
import './PassesPerStation.css';
import { generateInfo } from "./api";
import User from "./api";
import axios from "axios";


class PassesPerStation extends React.Component{
  constructor(props){
    super(props);

    this.state = {
      station: "",
      date_from: "",
      date_to: "",
      content: {},
      successful: null,
      message: null,
      url: null
    };

    this.handlestation = this.handlestation.bind(this);
    this.handledateto = this.handledateto.bind(this);
    this.handledatefrom = this.handledatefrom.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

handlestation(e){
  const name = e.target.name;
  const value = e.target.value;
  this.setState({ [name]: value});
}

handledateto(e){
  const name = e.target.name;
  const value = e.target.value;
  this.setState({ [name]: value});
}

handledatefrom(e){
  const name = e.target.name;
  const value = e.target.value;
  this.setState({ [name]: value});
}


 handleSubmit(e) {
    this.setState({ successful: null });

    if (this.state.station && this.state.datefrom && this.state.dateto) {
      // this.setState({ successful: 'smth' });
      let reqObj = {
        station: this.state.station,
        datefrom: this.state.datefrom,
        dateto: this.state.dateto
      };
      // generateInfo(reqObj)//return a json with info or null
      //   .then(response => {
      //       this.setState( {testok: response.data,
      //       successful: true
      //     });
      //   },
      //   error => {
      //     this.setState({
      //       content : "error"
      //     });
      //   }
      //   );
      // }

      const URL = 'http://127.0.0.1:9103/interoperability/api/PassesPerStation/' + reqObj.station + '/' + reqObj.datefrom + '/'+ reqObj.dateto ;
      this.setState({url: URL});
      axios.get(URL)
      .then( 
        response => {
          this.setState({
            content: response.data,
            successful: 'smth'
          });
        },
        error => {
          var resMessage =
            (error.response &&
              error.response.data &&
              error.response.data.message) ||
            error.message ||
            error.toString();

          if (resMessage == "Request failed with status code 402") resMessage = "There are no available sessions";
          if (resMessage == "Anauthorized") resMessage = "Please retry with a valid ID";
          this.setState({
            successful: 'smth2',
            content: [],
            message: resMessage
          });
        }
      );
    }
  }


  table1() {
    const data = new Array(this.state.content.PassesList.length);
    for (var j=0; j<this.state.content.PassesList.length; j++) data[j] = new Array(8);
    for (var j=0; j<this.state.content.PassesList.length; j++) {
      data[j][0] = this.state.content.PassesList[j].PassIndex;
      data[j][1] = this.state.content.PassesList[j].PassID;
      data[j][2] = this.state.content.PassesList[j].PassTimeStamp;
      data[j][3] = this.state.content.PassesList[j].VehicleId;
      data[j][4] = this.state.content.PassesList[j].TagProvider;
      data[j][5] = this.state.content.PassesList[j].PassType;
    }

    return (
      <div>
        <table>
          <thead id="station-table-data">
            <td><h3><b>Session Index</b></h3></td>
            <td><h3><b>Session ID</b></h3></td>
            <td><h3><b>Started On</b></h3></td>
            <td><h3><b>Finished On</b></h3></td>
            <td><h3><b>Protocol</b></h3></td>
            <td><h3><b>Energy Delivered</b></h3></td>
          </thead>
          <tbody id="station-table-data">
            {data.slice(0, data.length).map((item, index) => {
              return (
                <tr>
                  <td><h5>{item[0]}</h5></td>
                  <td><h5>{item[1]}</h5></td>
                  <td><h5>{item[2]}</h5></td>
                  <td><h5>{item[3]}</h5></td>
                  <td><h5>{item[4]}</h5></td>
                  <td><h5>{item[5]}</h5></td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    );
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
             onClick={this.handleSubmit}
             >
             Ok
             </button>

            {this.state.successful == null && (
            <div className="error">
              {this.state.successful}
            </div>
            )}

            {this.state.successful == true && (
            <div className="error">
              {this.state.successful}
            </div>
            )}

          {this.state.successful == 'smth' && (
            <div className="error">
              {this.state.successful}
              {this.state.content}
            </div>
            )}

          {this.state.successful == 'smth2' && (
            <div className="error">
              {this.state.successful}
              {this.state.message}
              {this.state.url}
            </div>
            )}

            {/* {this.state.successful && (
              <div className="form-group">
                <div id="response"
                  className={
                    this.state.successful
                      ? "alert alert-success"
                      : "alert alert-danger"
                  }
                  role="alert"
                >
                  <div className="welcome">
                    <h2> Stations Data : </h2>
                  </div>
                  <header className="jumbotron" id="getData">
                    {/* <h3> <b>Point</b>: {this.state.content.Point} </h3>
                    <h3> <b>Point Operator</b>: {this.state.content.PointOperator} </h3>
                    <h3> <b>Request Timestamp</b>: {this.state.content.RequestTimestamp} </h3>
                    <h3> <b>Period From</b>: {this.state.content.PeriodFrom} </h3>
                    <h3> <b>Period To</b>: {this.state.content.PeriodTo} </h3>
                    <h3> <b>Number Of Charging Sessions</b>: {this.state.content.NumberOfChargingSessions} </h3> */}
                    {/* <h3> <b>Passes Per Station</b>: </h3>
                    {this.table1()}
                  </header>
                  </div>
                </div>
            )}   */} */}
      </div>

    );

 }
}

export default PassesPerStation;