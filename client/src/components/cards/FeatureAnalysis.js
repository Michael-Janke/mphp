import React, { Component } from "react";
import RaisedButton from "material-ui/RaisedButton";
import Card from "../Card";
import Plot from "./Plot";
import Data from "./Data";
import styled from "styled-components";

class FeatureAnalysis extends Component {
  constructor(props) {
    super(props);
    this.state = { cards: [] };
  }

  render() {
    return (
      <div className="feature-analysis">
        <Card
          title={"Feature Analysis"}
          DataViewer={DataViewer}
          viewerProps={{ addCard: this.addCard.bind(this) }}
        />
        <StyledCards>{this.state.cards.map(this.renderCard)}</StyledCards>
      </div>
    );
  }

  renderCard(SpecifiedCard, index) {
    return <SpecifiedCard key={`card-${index}`} />;
  }

  addCard(SpecifiedCard) {
    this.setState({ cards: [...this.state.cards, SpecifiedCard] });
  }
}

class DataViewer extends Component {
  render() {
    return (
      <div className="menu">
        <StyledButton
          label="Show some data"
          primary={true}
          onClick={() => {
            this.props.addCard(Data);
          }}
        />
        <StyledButton
          label="Show some Plots"
          primary={true}
          onClick={() => {
            this.props.addCard(Plot);
          }}
        />
      </div>
    );
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

export default FeatureAnalysis;
