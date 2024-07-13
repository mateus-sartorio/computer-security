async function fetchStuff() {
  const response = await fetch("http://localhost:8080/graphql", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: '{ "query": "{ notices { edges { node { payload } } } }" }',
  });
  const result = await response.json();
  for (let edge of result.data.notices.edges) {
    let payload = edge.node.payload;
    console.log(payload)
  }
}

fetchStuff()