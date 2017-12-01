import React, { Component } from "react";
import RaisedButton from "material-ui/RaisedButton";
import Statistics from "./cards/Statistics";
import Plot from "./cards/Plot";
import Data from "./cards/Data";
import styled from "styled-components";

class Content extends Component {
  constructor(props) {
    super(props);
    this.state = { cards: [] };
  }

  render() {
    return (
      <StyledContent className="content">
        <div className="menu">
          <StyledButton
            label="Show statistics"
            primary={true}
            onClick={() => {
              this.addCard(Statistics);
            }}
          />
          <StyledButton
            label="Show some data"
            primary={true}
            onClick={() => {
              this.addCard(Data);
            }}
          />
          <StyledButton
            label="Show some Plots"
            primary={true}
            onClick={() => {
              this.addCard(Plot);
            }}
          />
        </div>
        <StyledCards>{this.state.cards.map(this.renderCard)}</StyledCards>
      </StyledContent>
    );
  }

  renderCard(Card, index) {
    return <Card key={`card-${index}`} />;
  }

  addCard(Card) {
    this.setState({ cards: [...this.state.cards, Card] });
  }
}

const StyledContent = styled.div`
  position: relative;
  top: ${props => props.theme.totalHeaderHeight};
`;

const StyledButton = styled(RaisedButton)`
  && {
    margin: 12px;
  }
  button {
    background: ${props => props.theme.boringBlue} !important;
  }
`;

const StyledCards = styled.div`
  display: flex;
  flex-wrap: wrap;
`;

export default Content;
