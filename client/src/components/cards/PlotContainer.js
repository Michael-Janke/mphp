import React, { Component } from "react";
import { connect } from "react-redux";

import { load } from "../../actions/plotActions";
import InteractivePlot from "./Plot";

const mapStateToProps = state => {
  return {
    plot: state.plot
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadPlot: (route, params) => {
      dispatch(load(route, params));
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(InteractivePlot);
