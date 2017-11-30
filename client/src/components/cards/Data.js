import React, { Component } from "react";
import { connect } from "react-redux";
import { load } from "../../actions/someDataActions";
import Card from "../Card";

const ROUTE = "/data";
const TITLE = "Some Data";

class Data extends Component {
  render() {
    return <Card route={ROUTE} title={TITLE} DataView={DataView} />;
  }
}

class DataView extends Component {
  render() {
    return <p>{JSON.stringify(this.props.data)}</p>;
  }
}

const mapStateToProps = state => {
  return {
    someData: state.someData
  };
};

const mapDispatchToProps = dispatch => {
  return {
    loadSomeData: () => {
      dispatch(load());
    }
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Data);
