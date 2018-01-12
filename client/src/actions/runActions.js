import * as types from "./actionTypes";
import { postRequest } from "./_request";
import { isHealthy } from "../utils";

export function createRun({ tcgaTokens, tissueTypes }) {
  return dispatch => {
    const id = Date.now();
    dispatch({ type: types.CREATE_RUN, id, tcgaTokens, tissueTypes });
  };
}

export function updateAlgorithm(id, algorithm) {
  return dispatch => {
    dispatch({ type: types.UPDATE_ALGORITHM, id, algorithm });
  };
}

export function toggleTcgaToken(id, algorithm, tcgaToken) {
  return dispatch => {
    dispatch({
      type: types.UPDATE_ALGORITHM,
      id,
      algorithm: {
        ...algorithm,
        cancerTypes: arrayToggle(algorithm.cancerTypes, tcgaToken)
      }
    });
  };
}

export function toggleTissueType(id, algorithm, tissueType) {
  return dispatch => {
    dispatch({
      type: types.UPDATE_ALGORITHM,
      id,
      algorithm: {
        ...algorithm,
        healthyTissueTypes: isHealthy(tissueType)
          ? arrayToggle(algorithm.healthyTissueTypes, tissueType)
          : algorithm.healthyTissueTypes,
        sickTissueTypes: !isHealthy(tissueType)
          ? arrayToggle(algorithm.sickTissueTypes, tissueType)
          : algorithm.sickTissueTypes
      }
    });
  };
}

export function runAlgorithm(id, algorithm) {
  return dispatch => {
    dispatch(startAlgorithm(id, algorithm));
    postRequest("/runAlgorithm", { algorithm })
      .then(response => dispatch(algorithmDone(id, response)))
      .then(() => dispatch(startEvaluation(id)))
      .then(() => postRequest("/evaluation", { ...algorithm }))
      .then(response => dispatch(evaluationDone(id, response)));

    function startAlgorithm(id, algorithm) {
      return { type: types.START_ALGORITHM, id, algorithm };
    }

    function algorithmDone(id, result) {
      return {
        type: types.ALGORITHM_DONE,
        id,
        result
      };
    }

    function startEvaluation(id) {
      return { type: types.START_EVALUATION, id };
    }

    function evaluationDone(id, evaluation) {
      return {
        type: types.EVALUATION_DONE,
        id,
        evaluation
      };
    }
  };
}

function arrayToggle(array, element) {
  return array.includes(element)
    ? array.filter(anElement => element !== anElement)
    : [...array, element];
}
