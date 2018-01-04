/* global Plotly:true */
import loadScript from "load-script";
import React, { Component } from "react";
import createPlotlyComponent from "react-plotly.js/factory";
import Color from "tinycolor2";

import { statisticsColors } from "../../config/colors";

let Plot;
loadScript("https://cdn.plot.ly/plotly-latest.min.js", function(err, script) {
  if (err) {
    console.warn(
      "Could not load plotly script from CDN, trying to load local script..."
    );
    loadScript("plotly-1.31.2.min.js", function(err, script) {
      if (err) {
        console.warn("Could not load plotly");
      } else {
        // note that in IE8 and below loading error wouldn't be reported
        Plot = createPlotlyComponent(Plotly);
      }
    });
  } else {
    // use script
    // note that in IE8 and below loading error wouldn't be reported
    Plot = createPlotlyComponent(Plotly);
  }
});

export default class InteractivePlot extends Component {
  rerender() {
    this.forceUpdate();
  }

  render() {
    const { data, genes } = this.props;
    let oldCancerType,
      oldColor,
      color,
      colorIndex = 0;
    const plotData = Object.keys(data).map((key, index) => {
      const cancerType = key.split("-")[0];
      if (oldCancerType != cancerType) {
        color = Color(statisticsColors[colorIndex++]);
        oldCancerType = cancerType;
        oldColor = color;
      } else {
        if (key.split("-")[1].includes("N")) {
          color = oldColor.spin(12).lighten(7);
        } else {
          color = oldColor.spin(-12).darken(7);
        }
        oldColor = color;
      }
      return {
        type: "scatter3d",
        mode: "markers",
        name: key,
        x: data[key][0],
        y: data[key][1],
        z: data[key][2],
        marker: {
          size: 5,
          color: color.toString(),
          opacity: 1
        }
      };
    });
    const plotLayout = {
      margin: {
        l: 0,
        r: 0,
        b: 0,
        t: 0
      },
      scene: {
        xaxis: {
          title: genes[0]
        },
        yaxis: {
          title: genes[1]
        },
        zaxis: {
          title: genes[2]
        }
      },
      legend: {
        yanchor: "middle",
        y: 0.7
      }
    };

    return (
      <div>
        <h3>Visualization</h3>
        <Plot data={plotData} layout={plotLayout} />
      </div>
    );
  }
}
