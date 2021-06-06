import { useQuery, gql } from "@apollo/client";
import "./App.css";

function App() {
  // initialize ApolloClient

  const QUERY_LINKS = gql`
    query {
      links {
        id
        url
      }
    }
  `;

  const { data, loading } = useQuery(QUERY_LINKS);
  if (loading) return <p>Loading...</p>;

  if (data) console.log(data);

  return <div className="App"></div>;
}

export default App;
