import React, { Component } from "react";
import styled from "styled-components";
import TooltipBox from "./TooltipBox";
import QuestionIcon from "material-ui/svg-icons/action/help-outline";
import WarningIcon from "material-ui/svg-icons/alert/warning";

export default class Description extends Component {
  render() {
    return (
      <Container>
        <ChildrenContainer>{this.props.children}</ChildrenContainer>
        <TooltipBox text={this.props.text} position={this.props.position}>
          {this.props.icon === "warning" ? <WarningIcon /> : <QuestionIcon />}
        </TooltipBox>
      </Container>
    );
  }
}

const Container = styled.div`
  display: flex;
  align-items: center;
`;

const ChildrenContainer = styled.div`
  label {
    white-space: nowrap;
  }
`;
