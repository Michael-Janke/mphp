import React, { Component } from "react";
import RaisedButton from "material-ui/RaisedButton";
import SelectField from "material-ui/SelectField";
import MenuItem from "material-ui/MenuItem";
import { connect } from "react-redux";
import { load } from "../../actions/featureAnalysisActions";
import Card from "../Card";
import Plot from "./Plot";
import Data from "./Data";
import styled from "styled-components";

class FeatureAnalysis extends Component {
  constructor(props) {
    super(props);
    this.state = { cards: [] };
    if (this.props.algorithms === null) {
      this.props.loadAlgorithms();
    }
  }

  render() {
    return (
      <div className="feature-analysis">
        <Card
          title={"Feature Analysis"}
          DataViewer={DataViewer}
          isLoading={!this.props.algorithms}
          viewerProps={{
            addCard: this.addCard.bind(this),
            algorithms: this.props.algorithms
          }}
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
  constructor(props) {
    super(props);
    this.state = { selectedAlgorithm: null };
  }

  render() {
    return (
      <div className="menu">
        <SelectField
          floatingLabelText="Algorithm"
          floatingLabelFixed={true}
          hintText="Select algorithm..."
          value={this.state.selectedAlgorithm}
          onChange={this.selectAlgorithm.bind(this)}
          autoWidth={true}
        >
          {this.props.algorithms.map(this.renderMenuItem)}
        </SelectField>
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

  renderMenuItem(algorithm, index) {
    return (
      <MenuItem
        key={`algorithm-option-${index}`}
        value={algorithm.key}
        primaryText={algorithm.name}
      />
    );
  }

  selectAlgorithm(event, index, selectedAlgorithm) {
    this.setState({ selectedAlgorithm });
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

const mapStateToProps = state => {
  return {
    ...state.featureAnalysis
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadAlgorithms: () => {
      dispatch(load());
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(FeatureAnalysis);
