import React, { Component } from "react";
import styled from "styled-components";

import Plot from "./Plot";
import Evaluation from "./Evaluation";
import GeneExploration from "./GeneExploration";
import Parameters from "./Parameters";

export default class Results extends Component {
  render() {
    const { result, algorithm, algorithms } = this.props;
    return (
      <div>
        <StyledParameters>
          <Parameters selectedAlgorithm={algorithm} algorithms={algorithms} />
        </StyledParameters>
        <StyledContent>
          <Plot {...result} />
          <Evaluation />
          <GeneExploration result={result} />
        </StyledContent>
      </div>
    );
  }
}

const StyledParameters = styled.div`
  margin: 0 16px 25px 16px;
`;

const StyledContent = styled.div`
  margin: 16px;
`;
