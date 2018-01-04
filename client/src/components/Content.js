import React, { Component } from "react";
import AlgorithmExecution from "./cards/AlgorithmExecutionContainer";
import Results from "./cards/ResultsContainer";

class Content extends Component {
  render() {
    return (
      <div className="content">
        <AlgorithmExecution />
        <Results />
      </div>
    );
  }
}

export default Content;
