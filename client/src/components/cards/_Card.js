import React, { Component } from 'react';
import { Card, CardTitle, CardText } from 'material-ui/Card';
import Spinner from '../Spinner';
import request from '../../request';
import constants from '../../constants';

class Content extends Component {
  constructor(props) {
    super(props);
    this.state = { isLoading: true, data: null };
  }

  componentDidMount() {
    request(this.props.route).then((data) => {
      this.setState({ isLoading: false, data });
    });
  }

  render() {
    return (
      <Card style={styles.card} zDepth={1}>
        {this.renderTitle()}
        {this.state.isLoading ? null : this.renderData()}
      </Card>
    );
  }

  renderTitle() {
    return (
      <CardTitle style={styles.cardTitle}>
        {this.props.title}
        {this.state.isLoading ? <Spinner style={styles.spinner} /> : null}
      </CardTitle>
    );
  }

  renderData() {
    const { DataView } = this.props;
    return (
      <CardText>
        <DataView data={this.state.data} />
      </CardText>
    );
  }
}

const styles = {
  card: {
    margin: constants.medium,
    padding: constants.medium,
    paddingVertical: constants.small,
  },
  cardTitle: {
    display: "flex",
    alignItems: "center",
    height: constants.cardTitleHeight,
  },
  spinner: {
    width: constants.cardTitleHeight,
    height: constants.cardTitleHeight,
    borderWidth: constants.cardTitleHeight / 2,
    marginLeft: constants.medium,
  },
}

export default Content;
