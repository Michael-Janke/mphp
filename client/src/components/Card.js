import React, { Component } from "react";
import { Card as _Card, CardTitle as _CardTitle, CardText as _CardText } from "material-ui/Card";
import Spinner from "./Spinner";
import styled from "styled-components";

const CARD_TITLE_HEIGHT = 15;

class Card extends Component {
  render() {
    const { title, data } = this.props;
    const isLoading = !data;
    return (
      <StyledCard zDepth={1}>
        <StyledCardTitle>
          <StyledTitleText>{title}</StyledTitleText>
          {isLoading ? <Spinner size={CARD_TITLE_HEIGHT} /> : null}
        </StyledCardTitle>
        {isLoading ? null : this.renderContent()}
      </StyledCard>
    );
  }

  renderContent() {
    const { data, DataViewer } = this.props;
    const isError = data && data.isError;
    return isError ? (
      <StyledError>{`${data.error}`}</StyledError>
    ) : (
      <DataViewer data={data} />
    );
  }
}

const StyledCard = styled(_Card)`
  width: fit-content;
  margin: ${props => props.theme.mediumSpace};
  padding: ${props => props.theme.mediumSpace};
  padding-top: ${props => props.theme.smallSpace};
  padding-bottom: ${props => props.theme.smallSpace};
`;

const StyledCardTitle = styled(_CardTitle)`
  display: flex;
  align-items: center;
  height: ${CARD_TITLE_HEIGHT};
`;

const StyledTitleText = styled.p`
  margin-right: ${props => props.theme.mediumSpace};
`;

const StyledError = styled(_CardText)`
  color: red !important;
`;

export default Card;
