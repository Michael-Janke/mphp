import React, { Component } from "react";
import { Card as _Card, CardTitle } from "material-ui/Card";
import FlatButton from 'material-ui/FlatButton';
import Dialog from 'material-ui/Dialog';
import styled from "styled-components";

import Spinner from "../Spinner";
import IconButton from "../IconButton";
import AlgorithmExecution from "./AlgorithmExecution";
import AlgorithmResult from "./AlgorithmResult";
import deepEqual from 'deep-equal';

const CARD_TITLE_HEIGHT = 15;

export default class Card extends Component {

  state = {
    open: false,
  };

  shouldComponentUpdate(nextProps, nextState) {
    if(nextState.open !== this.state.open) return true;    
    if(this.props.geneResult) return false; // will never change again
    if(nextProps.isLoading !== this.props.isLoading) return true;
    if(nextProps.dataset !== this.props.dataset) return true;
    if(nextProps.result !== null && this.props.result === null) return true;
    if(nextProps.geneResult !== null && this.props.geneResult === null) return true;
    return !deepEqual(nextProps.algorithm, this.props.algorithm);
  }

  handleOpen = () => {
    this.setState({open: true});
  };

  handleClose = (deleteIt = false) => {
    if(deleteIt) { this.props.deleteRun(this.props.runId); }
    this.setState({open: false});
  };

  startRun = () => {
    this.props.startRun(this.props.runId, {
      ...this.props.algorithm,
      dataset: this.props.dataset
    })
  }

  render() {
    const { isLoading, algorithm, datasets, dataset, result } = this.props;
    return (
      <StyledCard zDepth={1}>
        <StyledCardTitle>
          <StyledTitleText>
          {datasets[dataset] || ""} | {algorithm.name || "Execute Algorithm"}
          </StyledTitleText>
          {isLoading ? <Spinner size={CARD_TITLE_HEIGHT} /> : null}
          <IconButton icon="delete" onClick={this.handleOpen} />
          <Dialog
              actions={[<FlatButton label="No" primary={false}  onClick={this.handleClose.bind(this,false)} />,
                        <FlatButton label="Yes" primary={true}  onClick={this.handleClose.bind(this,true)} />]}
              modal={false}
              open={this.state.open}
              onRequestClose={this.handleClose.bind(this,false)}
            >
              Do you really want to delete this run?
          </Dialog>
        </StyledCardTitle>
        {this.renderBody()}
        {result && result.error ?
          <StyledError> {result.error.message} <FlatButton label="Retry" primary={true}  onClick={this.startRun.bind(this)} /> </StyledError>
        : null
        }
      </StyledCard>
    );
  }

  renderBody() {
    const { isError, isLoading, result } = this.props;
    if (isError) {
      return (
        <StyledError>Sorry, there was an error fetching the data.</StyledError>
      );
    }
    return (
      <div>
        <AlgorithmExecution
          {...this.props}
          disabled={isLoading || result !== null}
        />
        {result != null ? <AlgorithmResult {...this.props} /> : null}
      </div>
    );
  }
}

const StyledCard = styled(_Card)`
  margin: ${props => props.theme.mediumSpace};
  padding: ${props => props.theme.mediumSpace};
  padding-top: ${props => props.theme.smallerSpace};
  padding-bottom: ${props => props.theme.smallerSpace};
  min-width: 800px;
  max-width: 1000px;
  flex:1;
`;

const StyledCardTitle = styled(CardTitle)`
  display: flex;
  align-items: center;
  height: ${CARD_TITLE_HEIGHT}px;
`;

const StyledTitleText = styled.p`
  margin-right: ${props => props.theme.mediumSpace};
  font-size: ${props => props.theme.h2};
`;

const StyledError = styled.div`
  color: red;
`;
