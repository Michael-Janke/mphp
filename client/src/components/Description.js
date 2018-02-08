import React, { Component } from "react";
import styled from "styled-components";
import IconButton from "./IconButton";
import { deepGray } from "../config/colors";
import TooltipBox from "./TooltipBox";
import QuestionIcon from "material-ui/svg-icons/action/help-outline";

export default class Description extends Component {
  render() {
    return (
      <Container>
        <ChildrenContainer>{this.props.children}</ChildrenContainer>
        <TooltipBox text={this.props.text}>
          <QuestionIcon />
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
