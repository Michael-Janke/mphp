import React, { Component } from "react";
import Card from "../Card";
import DataSelection from "./DataSelection";
import AlgorithmSelection from "./AlgorithmSelection";

export default class AlgorithmExecution extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedAlgorithm: null,
      params: {}
    };
    if (this.props.algorithms === null) {
      this.props.loadAlgorithms();
    }
    if (this.props.statistics === null) {
      this.props.loadStatistics();
    }
  }

  render() {
    const {
      statistics,
      algorithms,
      tcgaTokens,
      tissueTypes,
      runAlgorithm,
      loadAlgorithms,
      loadStatistics
    } = this.props;
    return (
      <Card
        title={"Execute Algorithm"}
        isLoading={!this.props.statistics || !this.props.algorithms}
        isError={
          (this.props.statistics && this.props.statistics.isError) ||
          (this.props.algorithms && this.props.algorithms.isError)
        }
      >
        <AlgorithmSelection
          {...{
            algorithms,
            tcgaTokens,
            tissueTypes,
            loadAlgorithms,
            runAlgorithm
          }}
        />
        <DataSelection
          {...{ statistics, tcgaTokens, tissueTypes, loadStatistics }}
        />
      </Card>
    );
  }
}
