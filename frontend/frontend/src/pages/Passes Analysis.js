import React from "react";
import './PassesAnalysis.css';
import axios from "axios";


class PassesAnalysis extends React.Component{
  constructor(props){
    super(props);

    this.state = {
      op1: "",
      op2: "",
      date_from: "",
      date_to: "",
      content: {},
      clear: true,
      // bohthitika
      successful: null,
      message: null,
    };

    this.handleop1 = this.handleop1.bind(this);
    this.handleop2 = this.handleop2.bind(this);
    this.handledateto = this.handledateto.bind(this);
    this.handledatefrom = this.handledatefrom.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleClear = this.handleClear.bind(this);
   }

    handleop1(e){
      const name = e.target.name;
      const value = e.target.value;
      this.setState({ [name]: value});
    }

    handleop2(e){
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



    if (this.state.op1 && this.state.op2 && this.state.datefrom && this.state.dateto) {
      // this.setState({ successful: 'smth' });

      this.setState({clear:false});

      let reqObj = {
        op1: this.state.op1,
        op2: this.state.op2,
        datefrom: this.state.datefrom,
        dateto: this.state.dateto
      };

      const URL = 'http://127.0.0.1:9103/interoperability/api/PassesAnalysis/' + reqObj.op1 + '/'+ reqObj.op2 + '/' + reqObj.datefrom + '/'+ reqObj.dateto ;
      this.setState({url: URL});
      axios.get(URL)
      .then( 
        response => {
          this.setState({
            content: response.data,
            successful: 'yes'
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
            <th>Operator 1</th>
            <td><h5>{this.state.content.op1_ID}</h5></td>
          </tr>
          <tr>
            <th>Operator 2</th>
            <td><h5> {this.state.content.op2_ID}</h5></td>
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
      data[j][2] = this.state.content.PassesList[j].StationID;
      data[j][3] = this.state.content.PassesList[j].Timestamp;
      data[j][4] = this.state.content.PassesList[j].VevicleID;
      data[j][5] = this.state.content.PassesList[j].Charge;
    }

    return (
      <div>
        <table>
          <thead id="data_id">
          <tr>
            <th>Pass Index</th>
            <th>Pass id</th>
            <th>Station Id</th>
            <th>Timestamp</th>
            <th>Vehicle id</th>
            <th>Charge</th>
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
          <h1> Passes Analysis</h1>
          
          {/* NE*/}
          <input name="op1"
             field="op1"
             placeholder="op1"
             value={this.state.op1}
             onChange={this.handleop1}

              />

          <input name="op2"
             field="op2"
             placeholder="op2"
             value={this.state.op2}
             onChange={this.handleop2}

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
            

            {this.state.successful =='yes' && this.state.clear == false &&(
                <div id="response">

                  <header className="jumbotron" id="getData">
                    {this.minitable()}
                    <h2> Passes Analysis: </h2>
                    {this.table()} 
                    <button className="clear-button"
                      name="action"
                      onClick={this.handleClear}
                      >
                      Clear
                    </button>
                  </header>
                  </div>
            )}   
      </div>

    );

 }
}

export default PassesAnalysis;