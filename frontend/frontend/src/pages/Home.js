import React from 'react';
// import { render } from "react-dom";
import StationList from "./components/StationList";

function Home() {
  const styles = {
    fontFamily: "sans-serif",
    textAlign: "center"
  };

  return (

    <div className='home'>
      <h1>Home</h1>
      <h2>Select station {"\u2728"}</h2>
      <StationList /> 
    </div>
  );
}
export default Home;
