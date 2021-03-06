import React from "react";
import './PassesCost.css';
import axios from "axios";


class PassesCost extends React.Component{
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
      message: null
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

    this.setState({clear:false});

    if (this.state.op1 && this.state.op2 && this.state.datefrom && this.state.dateto) {
      let reqObj = {
        op1: this.state.op1,
        op2: this.state.op2,
        datefrom: this.state.datefrom,
        dateto: this.state.dateto
      };

      const URL = 'http://127.0.0.1:9103/interoperability/api/PassesCost/' + reqObj.op1 + '/'+ reqObj.op2 + '/' + reqObj.datefrom + '/'+ reqObj.dateto ;
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
          <tr>
            <th>Passes Cost</th>
            <td><h5>{this.state.content.PassesCost}</h5></td>
          </tr>
          </thead>
        </table>
      </div>
    );
  }
  
  

render() {
  return(
      <div className="new-form">
          <h1> Passes Cost</h1>
          
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


          {this.state.successful == 'no' && (
            <div className="error">
              {this.state.message}
            </div>
            )} 
            


            {this.state.successful =='yes' && this.state.clear == false &&(
                <div id="response">
                  <header className="jumbotron" id="getData">
                  <h2> Passes Cost: </h2>
                    {this.minitable()}

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

export default PassesCost;