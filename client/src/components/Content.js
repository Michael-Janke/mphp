import React, { Component } from "react";
import { connect } from "react-redux";
import { load as loadStatistics } from "../actions/statisticsActions";
import { loadAlgorithms, runAlgorithm } from "../actions/runActions";

import Card from "./Card";

class Content extends Component {
  constructor(props) {
    super(props);
    if (this.props.algorithms === null) {
      this.props.loadAlgorithms();
    }
    if (this.props.statistics === null) {
      this.props.loadStatistics();
    }
  }

  render() {
    const {
      runs,
      algorithms,
      statistics,
      tcgaTokens,
      tissueTypes,
      runAlgorithm
    } = this.props;
    return (
      <div className="content">
        {Object.keys(runs).map(runId => {
          const run = runs[runId];
          return (
            <Card
              key={runId}
              isLoading={!algorithms || !statistics || run.isLoading}
              isError={
                (statistics && statistics.isError) ||
                (algorithms && algorithms.isError)
              }
              runId={runId}
              params={run.params}
              result={run.result}
              algorithms={algorithms}
              statistics={statistics}
              tcgaTokens={tcgaTokens}
              tissueTypes={tissueTypes}
              runAlgorithm={runAlgorithm}
            />
          );
        })}
      </div>
    );
  }
}

const mapStateToProps = state => {
  return {
    runs: state.runs,
    algorithms: state.algorithms,
    statistics: state.statistics,
    tcgaTokens: state.dataSelection.tcgaTokens,
    tissueTypes: state.dataSelection.tissueTypes
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadAlgorithms: () => {
      dispatch(loadAlgorithms());
    },
    loadStatistics: () => {
      dispatch(loadStatistics());
    },
    runAlgorithm: (runId, params) => {
      dispatch(runAlgorithm(runId, params));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Content);
