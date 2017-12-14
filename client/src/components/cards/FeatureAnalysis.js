import React, { Component } from "react";
import RaisedButton from "material-ui/RaisedButton";
import SelectField from "material-ui/SelectField";
import MenuItem from "material-ui/MenuItem";
import TextField from "material-ui/TextField";
import styled, { withTheme } from "styled-components";
import { connect } from "react-redux";
import { load } from "../../actions/featureAnalysisActions";
import Card from "../Card";
import Plot from "./Plot";

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
          DataViewer={withTheme(DataViewer)}
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

  renderCard(card, index) {
    const SpecifiedCard = card.component;
    return <SpecifiedCard key={`card-${index}`} {...card.props} />;
  }

  addCard(card) {
    this.setState({ cards: [...this.state.cards, card] });
  }
}

class DataViewer extends Component {
  constructor(props) {
    super(props);
    this.state = { selectedAlgorithm: null };
  }

  render() {
    const runnable = this.state.selectedAlgorithm !== null;
    return (
      <StyledMenu>
        <StyledOptions>
          <SelectField
            floatingLabelText="Algorithm"
            floatingLabelFixed={true}
            hintText="Select algorithm..."
            value={runnable ? this.state.selectedAlgorithm.key : null}
            onChange={this.selectAlgorithm.bind(this)}
            autoWidth={true}
            selectedMenuItemStyle={{ color: this.props.theme.boringBlue }}
          >
            {this.props.algorithms.map(this.renderMenuItem)}
          </SelectField>
          {runnable
            ? this.state.selectedAlgorithm.parameters.map(
                this.renderParameter.bind(this)
              )
            : null}
        </StyledOptions>
        <StyledButton
          title={
            runnable
              ? `Run ${this.state.selectedAlgorithm.name}`
              : `Please select an algorithm`
          }
          label="Run"
          primary={true}
          onClick={() => {
            this.executeAlgorithm();
          }}
          disabled={!runnable}
        />
      </StyledMenu>
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

  renderParameter(parameter, index) {
    return (
      <StyledTextField
        key={`parameter-${index}`}
        defaultValue={parameter.default}
        hintText={parameter.default}
        floatingLabelText={parameter.name}
        floatingLabelFixed={true}
        type="number"
      />
    );
  }

  selectAlgorithm(event, index, key) {
    const selectedAlgorithm = this.props.algorithms.find(
      algorithm => algorithm.key === key
    );
    this.setState({ selectedAlgorithm });
  }

  executeAlgorithm() {
    const { selectedAlgorithm } = this.state;
    const cards = {
      getPCA: Plot,
      getDecisionTreeFeatures: Plot,
      getNormalizedFeaturesE: Plot,
      getNormalizedFeaturesS: Plot,
      getFeatures: Plot
    };
    const params = {
      key: "getPCA",
      cancerTypes: ["LUAD", "THCA"],
      sickTissueTypes: ["TP"],
      healthyTissueTypes: ["NT"],
      parameters: {
        components: 3,
        featuresPerComponent: 10
      }
    };
    this.props.addCard({
      component: cards[selectedAlgorithm.key],
      props: {
        route: `/runAlgorithm`,
        params
      }
    });
  }
}

const StyledButton = styled(RaisedButton)`
  && {
    margin: 12px;
  }
  button {
    background: ${props => props.theme.boringBlue} !important;
  }
  button:disabled {
    background: ${props => props.theme.lightGray} !important;
  }
`;

const StyledCards = styled.div`
  display: flex;
  flex-wrap: wrap;
`;

const StyledMenu = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const StyledOptions = styled.div`
  display: flex;
  align-items: center;
`;

const StyledTextField = styled(TextField)`
  margin-left: ${props => props.theme.mediumSpace};
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
