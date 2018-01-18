import React, { Component } from "react";
import { connect } from "react-redux";
import { updateName } from "../actions/experimentActions";
import { createRun } from "../actions/runActions";
import logo from "../assets/images/logo.png";
import styled from "styled-components";
import EditableText from "./EditableText";
import IconButton from "./IconButton";
import { almostWhite } from "../config/colors";

class Header extends Component {
  render() {
    return (
      <StyledHeaderContainer minimized={this.props.minimized}>
        <StyledHeader>
          <StyledLogo src={logo} />
          <StyledTitle>Clustered Gene Analysis</StyledTitle>
        </StyledHeader>
        <StyledExperimentHeader>
          <EditableText
            text={this.props.experimentName}
            onChange={this.props.updateExperimentName}
          />
          <div>
            <StyledRightContainer>
              <StyledText>{this.props.datasetName}</StyledText>
              <StyledSpacer />
              <StyledSpacer>|</StyledSpacer>
              <StyledSpacer />
              <IconButton
                tooltip="Open existing experiment"
                icon="open"
                color={almostWhite}
              />
              <StyledSpacer />
              <IconButton
                tooltip="Save experiment"
                icon="save"
                color={almostWhite}
              />
              <StyledSpacer />
              <IconButton
                tooltip="Add Card"
                icon="add"
                color={almostWhite}
                onClick={() => {
                  this.props.createRun(this.props.context);
                }}
              />
            </StyledRightContainer>
          </div>
        </StyledExperimentHeader>
      </StyledHeaderContainer>
    );
  }
}

const StyledSpacer = styled.div`
  margin-left: 3px;
  margin-right: 3px;
  color: ${props => props.theme.almostWhite};
`;

const StyledHeaderContainer = styled.div`
  position: absolute;
  display: flex;
  flex-direction: column;
  width: 100%;
  z-index: 9001; /* The z-index is over 9000! */
  transform: ${props =>
    props.minimized
      ? `translateY(-${props.theme.headerHeight})`
      : `translateY(0px)`};
  transition: transform 0.5s;
  overflow: hidden;
`;

const StyledHeader = styled.div`
  background-color: ${props => props.theme.boringBlue};
  height: ${props => props.theme.headerHeight};
  padding-left: ${props => props.theme.largeSpace};
  padding-right: ${props => props.theme.largeSpace};
  display: flex;
  align-items: center;
`;

const StyledExperimentHeader = styled.div`
  background-color: ${props => props.theme.slightlyBoringBlue};
  height: ${props => props.theme.experimentHeaderHeight};
  padding-left: ${props => props.theme.largeSpace};
  padding-right: ${props => props.theme.largeSpace};
  display: flex;
  align-items: center;
`;

const StyledTitle = styled.h1`
  margin: 0;
  margin-left: 20px;
  color: ${props => props.theme.almostWhite};
  font-size: ${props => props.theme.h1};
`;

const StyledLogo = styled.img`
  height: 45px;
`;

const StyledText = styled.p`
  color: ${props => props.theme.almostWhite};
  padding: ${props => props.theme.smallSpace};
  margin: 0;
  text-align: right;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  max-width: 200px;
`;

const StyledRightContainer = styled.div`
  display: flex;
  align-items: center;
`;

const mapStateToProps = state => {
  return {
    experimentName: state.experiment.name,
    datasetName: state.experiment.datasets[state.experiment.dataset],
    context: state.context
  };
};

const mapDispatchToProps = dispatch => {
  return {
    updateExperimentName: newName => {
      dispatch(updateName(newName));
    },
    createRun: context => {
      dispatch(createRun(context));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Header);
