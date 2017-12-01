import React, { Component } from "react";
import styled from "styled-components";
import _IconButton from 'material-ui/IconButton';
import EditIcon from 'material-ui/svg-icons/editor/mode-edit';

class IconButton extends Component {
  render() {
    const icons = {
        edit: EditIcon
    };
    const Icon = icons[this.props.icon]

    return (
      <StyledIconButton tooltip={this.props.tooltip} color={this.props.color} onClick={this.props.onClick}>
        <Icon />
      </StyledIconButton>
    );
  }
}

const StyledIconButton = styled(_IconButton)`
    width: 38px !important;
    height: 38px !important;
    padding: 9px !important;
    margin-left: 6px !important;
    svg {
        width: 19px !important;
        height: 19px !important;
        color: ${props => props.color} !important;
    }
`;

export default IconButton;
