import React from "react";
import './PassesPerStation.css';
import axios from "axios";


class PassesPerStation extends React.Component{
  constructor(props){
    super(props);

    this.state = {
      station: "",
      date_from: "",
      date_to: "",
      content: {},
      clear: true,
      // bohthitika
      successful: null,
      message: null
    };

    this.handlestation = this.handlestation.bind(this);
    this.handledateto = this.handledateto.bind(this);
    this.handledatefrom = this.handledatefrom.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleClear = this.handleClear.bind(this);
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

    handleClear(e){
      this.setState({clear: true});
    }

  handleSubmit(e) {
    this.setState({ successful: null });

    if (this.state.station && this.state.datefrom && this.state.dateto) {

      this.setState({clear:false});

      let reqObj = {
        station: this.state.station,
        datefrom: this.state.datefrom,
        dateto: this.state.dateto
      };

      const URL = 'http://127.0.0.1:9103/interoperability/api/PassesPerStation/' + reqObj.station + '/' + reqObj.datefrom + '/'+ reqObj.dateto ;
      this.setState({url: URL});
      axios.get(URL)
      .then( 
        response => {
          this.setState({
            content: response.data,
            successful: "yes"
          });
        },
        error => {
          var resMessage =
            (error.response &&
              error.response.data &&
              error.response.data.message) ||
            error.message ||
            error.toString();
          if (resMessage == "Request failed with status code 400") resMessage = "Request failed with status code 400-Bad Request"
          if (resMessage == "Request failed with status code 402") resMessage = "Request failed with status code 402-No Data";
          if (resMessage == "Request failed with status code 500") resMessage = "Request failed with status code 500-Interval Server Error";
          this.setState({
            successful: 'no',
            content: [],
            message: resMessage
          });
        }
      );
    }

    else{
      this.setState({
      successful: 'no',
      message: "Request failed with status code 400-Bad Request"
      })

    }
  }

  minitable(){
    return (
      <div>
        <table>
          <thead id="data_id">
          <tr>
            <th>Station</th>
            <td><h5>{this.state.content.Station}</h5></td>
          </tr>
          <tr>
            <th>Station Operator</th>
            <td><h5> {this.state.content.StationOperator}</h5></td>
          </tr>
          <tr>
            <th>Request Timestamp</th>
            <td><h5>{this.state.content.RequestTimestamp}</h5></td>
          </tr>
          <tr>
            <th>Period From</th>
            <td><h5>{this.state.content.PeriodFrom}</h5></td>
          </tr>
          <tr>
            <th>Period To</th>
            <td><h5> {this.state.content.PeriodTo} </h5></td>
          </tr>
          <tr>
            <th>Number of Passes</th>
            <td><h5>{this.state.content.NumberOfPasses}</h5></td>
            </tr>
          </thead>
        </table>
      </div>
    );
  }
  
  table() {
    const data = new Array(this.state.content.PassesList.length);
    for (var j=0; j<this.state.content.PassesList.length; j++) data[j] = new Array(6);
    for (var j=0; j<this.state.content.PassesList.length; j++) {
      data[j][0] = this.state.content.PassesList[j].PassIndex;
      data[j][1] = this.state.content.PassesList[j].PassId;
      data[j][2] = this.state.content.PassesList[j].PassTimeStamp;
      data[j][3] = this.state.content.PassesList[j].VevicleID;
      data[j][4] = this.state.content.PassesList[j].TagProvider;
      data[j][5] = this.state.content.PassesList[j].PassType;
    }

    return (
      <div>
        <table>
          <thead id="data_id">
          <tr>
            <th>Pass Index</th>
            <th>Contact</th>
            <th>Country</th>
            <th>Pass Index</th>
            <th>Contact</th>
            <th>Country</th>
          </tr>
          </thead>
          <tbody id="data_id">
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
          
          {/* NE01 */}
          <input name="station"
             field="station"
             placeholder="station"
             value={this.state.station}
             onChange={this.handlestation}

              />
          {/* 20000102 */}
          <input name="datefrom"
            type="datefrom"
            field="datefrom"
            placeholder="datefrom"
            value={this.state.datefrom}
            onChange={this.handledatefrom}
            />
          {/* 20190102 */}
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


          {this.state.successful == 'no' && (
            <div className="error">
              {this.state.message}
            </div>
            )} 
            

            {this.state.successful =='yes' && this.state.clear== false &&(
              // <div className="form-group">
                <div id="response"
                  // className={
                  //   this.state.successful
                  //     ? "alert alert-success"
                  //     : "alert alert-danger"
                  // }
                  // role="alert"
                >
                  {/* <div className="welcome">
                   
                  </div> */}
                  <header className="jumbotron" id="getData">
                  <h2> Information for: </h2>
                    {this.minitable()}
                    <h2> Passes Per Station: </h2>
                    {this.table()} 
                    <button className="clear-button"
                      name="action"
                      onClick={this.handleClear}
                      >
                      Clear
                    </button>
                  </header>


                 
                  </div>

                // </div>
            )}   
      </div>

    );

 }
}

export default PassesPerStation;