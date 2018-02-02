import React, { Component } from "react";
import styled from "styled-components";

import Plot from "./Plot";
import Evaluation from "./Evaluation";
import GeneExploration from "./GeneExplorationContainer";

export default class Results extends Component {
  render() {
    // TODO render tabs for oneAgainstRest results
    let { result, runId, oneAgainstRest } = this.props;
    if (oneAgainstRest) {
      result = result.isError ? result : result[Object.keys(result)[0]];
    }
    return (
      <div>
        {!result.isError ? (
          <StyledContent>
            <Columns>
              <Plot {...result} />
              <Evaluation {...result.evaluation} />
            </Columns>
            <GeneExploration runId={runId} {...result} />
          </StyledContent>
        ) : (
          <div>Server error</div>
        )}
      </div>
    );
  }
}

const StyledContent = styled.div`
  margin: 16px;
`;

const Columns = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-around;
`;
