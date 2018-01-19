import React, { Component } from "react";
import { connect } from "react-redux";
import { loadContext } from "../actions/contextActions";
import { runAlgorithm, updateAlgorithm } from "../actions/runActions";
import Spinner from "./Spinner"

import Run from "./Run";

class Content extends Component {
  constructor(props) {
    super(props);
    const context = this.props.context;
    if (context === null) {
      this.props.loadContext();
    }
  }

  render() {
    const { runs, context, runAlgorithm, updateAlgorithm, dataset } = this.props;
    const { isError, datasets, statistics, algorithms } = context || {};
    return (
      <div className="content">
        {dataset && datasets ? 
          Object.keys(runs)
            .reverse()
            .map(runId => {
              const { algorithm, result, isLoading } = runs[runId];
              return (
                <Run
                  key={runId}
                  isLoading={!algorithms || !statistics || isLoading}
                  isError={isError}
                  runId={runId}
                  algorithm={algorithm}
                  result={result}
                  runAlgorithm={runAlgorithm}
                  updateAlgorithm={updateAlgorithm}
                  algorithms={algorithms}
                  dataset={dataset}
                  {...statistics[dataset]}
                />
              );
            }) : 
            <Spinner />
        }
      </div>
    );
  }
}

const mapStateToProps = state => {
  return {
    runs: state.runs,
    context: state.context,
    dataset: state.experiment.dataset
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadContext: () => {
      dispatch(loadContext());
    },
    runAlgorithm: (runId, params) => {
      dispatch(runAlgorithm(runId, params));
    },
    updateAlgorithm: (runId, params) => {
      dispatch(updateAlgorithm(runId, params));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Content);
