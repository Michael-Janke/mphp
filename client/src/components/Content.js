import React, { Component } from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import Card from './Card';

const STATISTICS_CARD = {
  route: "/statistics",
  title: "Statistics",
};

const DATA_CARD = {
  route: "/data",
  title: "Some Data",
};

class Content extends Component {
  constructor(props) {
    super(props);
    this.state = { cards: [] };
  }

  render() {
    return (
      <div className="content">
        <div className="menu">
           <RaisedButton
             label="Show statistics"
             primary={true}
             style={styles.button}
             onClick={() => { this.addCard(STATISTICS_CARD); }}
          />
           <RaisedButton
             label="Show some data"
             primary={true}
             style={styles.button}
             onClick={() => { this.addCard(DATA_CARD); }}
          />
        </div>
        <div className="cards">
          {this.state.cards.map(this.renderCard)}
        </div>
      </div>
    );
  }

  renderCard(card, index) {
    return <Card key={`card-${index}`} {...card} />
  }

  addCard(card) {
    this.setState({ cards: [ ...this.state.cards, card ]});
  }
}

const styles = {
  button: {
    margin: 12,
  },
};

export default Content;
