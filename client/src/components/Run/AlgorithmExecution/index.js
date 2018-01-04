import React, { Component } from "react";
import DataSelection from "./DataSelection";
import AlgorithmSelection from "./AlgorithmSelection";

export default class AlgorithmExecution extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedAlgorithm: null,
      params: {}
    };
  }

  render() {
    const {
      statistics,
      algorithms,
      tcgaTokens,
      tissueTypes,
      runAlgorithm,
      loadAlgorithms,
      loadStatistics,
      runId,
      toggleLoading
    } = this.props;
    return (
      <div>
        <AlgorithmSelection
          {...{
            algorithms,
            tcgaTokens,
            tissueTypes,
            loadAlgorithms,
            runAlgorithm,
            runId,
            toggleLoading
          }}
        />
        <DataSelection
          {...{ statistics, tcgaTokens, tissueTypes, loadStatistics }}
        />
      </div>
    );
  }
}
