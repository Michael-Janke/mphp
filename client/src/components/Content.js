import React, { Component } from "react";
import RaisedButton from "material-ui/RaisedButton";
import Statistics from "./cards/Statistics";
import Plot from "./cards/Plot";
import Data from "./cards/Data";
import styled from "styled-components";
import SelectDataset from "./cards/SelectDataset";
import DataSelection from "./cards/DataSelection";

class Content extends Component {
  constructor(props) {
    super(props);
    this.state = { cards: [] };
  }

  render() {
    return (
      <div className="content">
        <SelectDataset title="Your Dataset:" data="DATA SET 4" />
        <DataSelection />
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
      </div>
    );
  }

  renderCard(Card, index) {
    return <Card key={`card-${index}`} />;
  }

  addCard(Card) {
    this.setState({ cards: [...this.state.cards, Card] });
  }
}

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
