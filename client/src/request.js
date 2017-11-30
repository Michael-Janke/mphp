const serverUrl = "http://localhost:5000";

export default route => {
  // TODO error handling
  return fetch(`${serverUrl}${route}`)
    .then(response => response.json())
    .then(json => json)
    .catch(error => console.log(error));
};
