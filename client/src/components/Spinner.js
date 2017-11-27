import React, { Component } from 'react';
import constants from '../constants';

class Spinner extends Component {
  render() {
    return <div className="spinner" style={{...styles.spinner, ...this.props.style}} />;
  }
}

const styles = {
  spinner: {
    height: 40,
    width: 40,
    border: "20px solid " + constants.gray,
    borderTop: "20px solid " + constants.blue,
    borderRadius: "50%",
    animation: "spin 2s linear infinite", // spin defined in index.css
  },
}

export default Spinner;
