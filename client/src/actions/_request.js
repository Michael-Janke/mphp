const SERVER_URL = "http://localhost:5000";

export default route => {
  return fetch(`${SERVER_URL}${route}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }
      return response.json();
    })
    .then(json => json)
    .catch(error => {
      console.error(error);
      return { isError: true, error };
    });
};
