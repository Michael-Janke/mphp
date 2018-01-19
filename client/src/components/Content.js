import React, { Component } from "react";
import { connect } from "react-redux";
import styled from "styled-components";
import FlatButton from 'material-ui/FlatButton';
import Dialog from 'material-ui/Dialog';
import { loadContext } from "../actions/contextActions";
import { startRun, updateRun, deleteRun } from "../actions/runActions";
import Spinner from "./Spinner"

import Run from "./Run";

class Content extends Component {
  constructor(props) {
    super(props);
    const context = this.props.context;
    if (!context.datasets) {
      this.props.loadContext();
    }
  }

  render() {
    const { runs, context, startRun, updateRun, deleteRun } = this.props;
    return (
      <div className="content">
        { context.datasets ? 
          Object.keys(runs)
            .reverse()
            .map(runId => {
              const run = runs[runId];
              return (
                <Run
                  key={runId}
                  runId={runId}
                  {...run}
                  startRun={startRun}
                  updateRun={updateRun}
                  deleteRun={deleteRun}
                  {...context}
                />
              );
            }) : 
            <Dialog
                actions={[<FlatButton label="Retry" primary={true} disabled={!context.isError} onClick={this.props.loadContext} />]}
                modal={false}
                open={!context.datasets}
              >
                 {context.isError ? 
                    <LoadingText>Couldn't load context data. Retry? ({context.error.message})</LoadingText> : 
                    <StyledSpinnerContainer>
                      <Spinner size={20} />
                      <LoadingText>loading context data</LoadingText>
                    </StyledSpinnerContainer>
                 }
            </Dialog>
        }
      </div>
    );
  }
}

const StyledSpinnerContainer = styled.div`
  display:flex;
  flex-direction: row;
  align-items: center;
  height: 100px;
`;

const LoadingText = styled.div`
  font-size: ${props => props.theme.h1};
  margin-left: 10px;
`;

const mapStateToProps = state => {
  return {
    runs: state.runs,
    context: state.context,
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadContext: () => {
      dispatch(loadContext());
    },
    startRun: (runId, params) => {
      dispatch(startRun(runId, params));
    },
    deleteRun: (runId) => {
      dispatch(deleteRun(runId));
    },
    updateRun: (runId, params) => {
      dispatch(updateRun(runId, params));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Content);
