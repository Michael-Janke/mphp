import React, { Component } from "react";
import styled from "styled-components";
import _IconButton from "material-ui/IconButton";
import EditIcon from "material-ui/svg-icons/editor/mode-edit";
import OpenIcon from "material-ui/svg-icons/file/folder-open";
import SaveIcon from "material-ui/svg-icons/content/save";
import AddIcon from "material-ui/svg-icons/content/add-circle";

class IconButton extends Component {
  render() {
    const icons = {
      edit: EditIcon,
      open: OpenIcon,
      save: SaveIcon,
      add: AddIcon
    };
    const Icon = icons[this.props.icon];

    return (
      <StyledIconButton
        tooltip={this.props.tooltip}
        color={this.props.color}
        onClick={this.props.onClick}
      >
        <Icon />
      </StyledIconButton>
    );
  }
}

const StyledIconButton = styled(_IconButton)`
  width: 38px !important;
  height: 38px !important;
  padding: ${props => props.theme.smallSpace} !important;
  svg {
    width: 19px !important;
    height: 19px !important;
    color: ${props => props.color || props.textColor} !important;
  }
`;

export default IconButton;
