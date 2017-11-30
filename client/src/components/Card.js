import React, { Component } from "react";
import { Card, CardTitle, CardText } from "material-ui/Card";
import Spinner from "./Spinner";
import request from "../request";
import styled from "styled-components";

const CARD_TITLE_HEIGHT = 15;

class Content extends Component {
  constructor(props) {
    super(props);
    this.state = { isLoading: true, data: null };
  }

  componentDidMount() {
    request(this.props.route).then(data => {
      this.setState({ isLoading: false, data });
    });
  }

  render() {
    return (
      <StyledCard zDepth={1}>
        {this.renderTitle()}
        {this.state.isLoading ? null : this.renderData()}
      </StyledCard>
    );
  }

  renderTitle() {
    return (
      <StyledCardTitle>
        <StyledTitleText>{this.props.title}</StyledTitleText>
        {this.state.isLoading ? <Spinner size={CARD_TITLE_HEIGHT} /> : null}
      </StyledCardTitle>
    );
  }

  renderData() {
    const { DataView } = this.props;
    return (
      <CardText>
        <DataView data={this.state.data} />
      </CardText>
    );
  }
}

const StyledCard = styled(Card)`
  width: fit-content;
  margin: ${props => props.theme.mediumSpace};
  padding: ${props => props.theme.mediumSpace};
  padding-top: ${props => props.theme.smallSpace};
  padding-bottom: ${props => props.theme.smallSpace};
`;

const StyledCardTitle = styled(CardTitle)`
  display: flex;
  align-items: center;
  height: ${CARD_TITLE_HEIGHT};
`;

const StyledTitleText = styled.p`
  margin-right: ${props => props.theme.mediumSpace};
`;

export default Content;
