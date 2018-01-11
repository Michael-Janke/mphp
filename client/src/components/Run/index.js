import React, { Component } from "react";
import { Card as _Card, CardTitle } from "material-ui/Card";
import styled from "styled-components";

import Spinner from "../Spinner";
import AlgorithmExecution from "./AlgorithmExecution";
import AlgorithmResult from "./AlgorithmResult";

const CARD_TITLE_HEIGHT = 15;

export default class Card extends Component {
  render() {
    const { isLoading, algorithm } = this.props;
    return (
      <StyledCard zDepth={1}>
        <StyledCardTitle>
          <StyledTitleText>
            {algorithm.name || "Execute Algorithm"}
          </StyledTitleText>
          {isLoading ? <Spinner size={CARD_TITLE_HEIGHT} /> : null}
        </StyledCardTitle>
        {this.renderBody()}
      </StyledCard>
    );
  }

  renderBody() {
    const { isError, isLoading, result } = this.props;
    if (isLoading) return null;
    if (isError) {
      return (
        <StyledError>Sorry, there was an error fetching the data.</StyledError>
      );
    }
    return (
      <div>
        <AlgorithmExecution {...this.props} disabled={result != null} />
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
