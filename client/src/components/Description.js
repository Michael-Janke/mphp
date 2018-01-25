import React, { Component } from "react";
import styled from "styled-components";
import IconButton from "./IconButton";
import { deepGray } from "../config/colors";

export default class Description extends Component {
  render() {
    return (
      <Container>
        <ChildrenContainer>{this.props.children}</ChildrenContainer>
        <IconButton
          icon="help"
          tooltip={this.props.text}
          tooltipPosition={"bottom-right"}
          color={deepGray}
          cursor={"default"}
          padding={"0px"}
          size={"28px"}
        />
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
