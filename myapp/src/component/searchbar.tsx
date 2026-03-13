import React, { useState } from "react";
//You will need to watch some youtube videos on how to use the fetch API to call the backend API and get the search results and display them in the UI. You can also refer to the homepage.tsx file for an example of how to call the backend API and display the results in a table.
// the purpose of this is to let you understand how our project function so I can't do more for you
//FEEL FREE TO MODIFY MY CODE IF NEEDED AS THIS IS JUST A TEMPLATE FOR YOU TO START WITH YOUR APPROACH MIGHT BE DIFFERENT THAN MINE.
//ASK ME IF YOU NEED EXTRA HELP OR CLARIFICATION ON HOW TO IMPLEMENT THIS COMPONENT.
function SearchBar() {
  //here to call the backend API to get the search results and store them in the state
  //For this i would say just use the stocck key to search stocks.
  //Use the same API endpoint as the homepage.tsx to get the stock data and then filter the results based on the search query.
  const [results, setResults] = useState(null);
  const handleSearch = async () => {
    fetch("http://localhost:5000/stocks")
      .then((response) => response.json())
      .then((data) => setResults(data))
      .catch((error) => console.error("Error fetching search results:", error));
  };

  return (
    //UI for the search bar, can be a simple input field and a button to trigger the search
    <div className="search-bar"></div>
  );
}
export default SearchBar;
