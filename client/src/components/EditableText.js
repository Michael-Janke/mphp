import React, { Component } from "react";
import styled, { withTheme } from "styled-components";
import IconButton from "./IconButton";

class EditableText extends Component {
  constructor(props) {
    super(props);
    this.state = {
      text: "Epic Experiment",
      isEditing: false
    };
  }

  render() {
    return (
      <StyledContainer>
        {this.renderText()}
        {this.renderIcon()}
      </StyledContainer>
    );
  }

  renderText() {
    return this.state.isEditing ? (
      <StyledInput
        type="text"
        autoFocus="true"
        onFocus={this.handleFocus}
        onBlur={this.stopEditing.bind(this)}
        value={this.state.text}
        onChange={this.updateText.bind(this)}
        onKeyPress={this.handleKeyPress.bind(this)}
      />
    ) : (
      <StyledExperimentName>{this.state.text}</StyledExperimentName>
    );
  }

  renderIcon() {
    return this.state.isEditing ? null : (
      <IconButton
        tooltip="Edit experiment name"
        icon="edit"
        color={this.props.theme.almostWhite}
        onClick={this.edit.bind(this)}
      />
    );
  }

  edit() {
    this.setState({ isEditing: true });
  }

  stopEditing() {
    this.setState({ isEditing: false });
  }

  handleFocus(event) {
    event.target.select();
  }

  updateText(event) {
    this.setState({ text: event.target.value });
  }

  handleKeyPress(event) {
    if (event.key === "Enter") {
      this.stopEditing();
    }
  }
}

const StyledExperimentName = styled.div`
  color: ${props => props.theme.almostWhite};
  font-size: ${props => props.theme.h2};
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
`;

const StyledInput = styled.input`
  width: 100%;
  font-family: Roboto;
  font-size: ${props => props.theme.h2};
  border: none;
  color: ${props => props.theme.almostWhite};
  background-color: ${props => props.theme.slightlyBoringBlue};
  :focus {
    outline: none;
  }
  ::selection {
    background: ${props => props.theme.boringBlue};
  }
`;

const StyledContainer = styled.div`
  width: 80%;
  display: flex;
  align-items: center;
`;

export default withTheme(EditableText);
