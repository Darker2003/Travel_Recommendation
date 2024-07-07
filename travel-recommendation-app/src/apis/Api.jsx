import axios from "axios";
// Define the API endpoint
const apiEndpoint = 'http://127.0.0.1:8000/destination/data/';

// Function to fetch data from the API
export const fetchData = async () => {

  const response = await axios.get(apiEndpoint);
  const data = response.data;
  return data
}