import React, { Component } from "react";
import { Card as _Card, CardTitle } from "material-ui/Card";
import Spinner from "./Spinner";
import styled from "styled-components";

const CARD_TITLE_HEIGHT = 15;

export default class Card extends Component {
  render() {
    const { title, isLoading, width, isError, className } = this.props;
    return (
      <StyledCard className={className} zDepth={1} width={width}>
        <StyledCardTitle>
          <StyledTitleText>{title}</StyledTitleText>
          {isLoading ? <Spinner size={CARD_TITLE_HEIGHT} /> : null}
        </StyledCardTitle>
        {isError ? (
          <StyledError>
            Sorry, there was an error fetching the data.
          </StyledError>
        ) : isLoading ? null : (
          this.props.children
        )}
      </StyledCard>
    );
  }
}

const StyledCard = styled(_Card)`
  width: ${props => (props.fitContent ? "fit-content" : null)};
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
