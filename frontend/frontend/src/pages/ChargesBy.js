import React from "react";
import './ChargesBy.css';
import axios from "axios";


class ChargesBy extends React.Component{
  constructor(props){
    super(props);

    this.state = {
      op1: "",
      date_from: "",
      date_to: "",
      content: {},
      // bohthitika
      successful: null,
      message: null,
      url: null
    };

    this.handleop1 = this.handleop1.bind(this);
    this.handledateto = this.handledateto.bind(this);
    this.handledatefrom = this.handledatefrom.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
   }

    handleop1(e){
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

    if (this.state.op1 && this.state.datefrom && this.state.dateto) {
      // this.setState({ successful: 'smth' });
      let reqObj = {
        op1: this.state.op1,
        datefrom: this.state.datefrom,
        dateto: this.state.dateto
      };

      const URL = 'http://127.0.0.1:9103/interoperability/api/ChargesBy/' + reqObj.op1 + '/' + reqObj.datefrom + '/'+ reqObj.dateto ;
      this.setState({url: URL});
      axios.get(URL)
      .then( 
        response => {
          this.setState({
            content: response.data,
            successful: 'y'
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
            successful: 'n',
            content: [],
            message: resMessage
          });
        }
      );
    }
    else{
      this.setState({
      successful: 'x'
      })
    }
  }

  minitable(){
    return (
      <div>
        <table>
          <thead id="data_id">
          <tr>
            <th>Operator Id</th>
            <td><h5>{this.state.content.op_ID}</h5></td>
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
          </thead>
        </table>
      </div>
    );
  }
  
  table() {
    const data = new Array(this.state.content.PPOList.length);
    for (var j=0; j<this.state.content.PPOList.length; j++) data[j] = new Array(3);
    for (var j=0; j<this.state.content.PPOList.length; j++) {
      data[j][0] = this.state.content.PPOList[j].VisitingOperator;
      data[j][1] = this.state.content.PPOList[j].NumberOfPasses;
      data[j][2] = this.state.content.PPOList[j].PassesCost;
    }

    return (
      <div>
        <table>
          <thead id="data_id">
          <tr>
            <th>Visiting Operator</th>
            <th>Number of Passes</th>
            <th>Passes Cost</th>
          </tr>
          </thead>
          <tbody id="data_id">
            {data.slice(0, data.length).map((item, index) => {
              return (
                <tr>
                  <td><h5>{item[0]}</h5></td>
                  <td><h5>{item[1]}</h5></td>
                  <td><h5>{item[2]}</h5></td>
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
          <h1> ChargesBy</h1>
          
          {/* NE01 */}
          <input name="op1"
             field="op1"
             placeholder="op1"
             value={this.state.op1}
             onChange={this.handleop1}

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


          {this.state.successful == 'n' && (
            <div className="error">
              {this.state.successful}
              {this.state.message}
              {this.state.url}
            </div>
            )} 
            
            {this.state.successful == 'x' && (
            <div className="error">
              {this.state.successful}
            </div>
            )}

            {this.state.successful =='y' && (
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
                   
                  </div>
                  <header className="jumbotron" id="getData">
                    {this.minitable()}
                    <h2> Charges By: </h2>
                    {this.table()} 
                  </header>
                  </div>
                </div>
            )}   
      </div>

    );

 }
}

export default ChargesBy;