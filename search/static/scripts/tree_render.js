$(document).ready(function () {
  const searchBtn = $('div#search');
  const queryInput = $('input#query_input');

  // Use click to listen to events
  searchBtn.on('click', function (event) {
    if (queryInput.val()) {
      alert('Processing result for:' + queryInput.val());
      search(queryInput.val());
    }
  });
  queryInput.on('keydown', function (event) {
    if (event.type === 'Enter') {
      alert('Fetching query results...');
      search(queryInput.val());
    }
  });

  // Make an AJAX request to get search results
  function search (query) {
    $.ajax({
      url: 'http://127.0.0.1:5000/search',
      method: 'POST',
      data: JSON.stringify({ q: query }),
      contentType: 'application/json',
      success: function (data) {
        // Process the search results and render in a tree structure
        renderSearchResults(data);
      },
      error: function () {
        alert('Unable to fetch query results'); // It will be removed later - Fixed the error message
      }
    });
  }

  function renderSearchResults (results) {
    const $resultsContainer = $('#results');
    $resultsContainer.empty();

    // Loop through the results from different search engines
    for (let i = 0; i < results.length; i++) {
      const engineName = results[i].engine;
      const engineResults = results[i].results;

      // Create a tree structure for each search engine
      const $engineNode = $('<div class="engine-node">');
      const $engineHeader = $('<div class="engine-header">').text(engineName);
      const $resultsList = $('<ul>');

      // Loop through the individual search results
      for (let j = 0; j < engineResults.length; j++) {
        const result = engineResults[j];
        const $resultNode = $('<li>').html(`<a href="${result.link}">${result.title}</a>  -  ${result.domain} <div>${result.description}</div>`);
        $resultsList.append($resultNode);
      }
      $engineNode.append($engineHeader, $resultsList);
      $resultsContainer.append($engineNode);
    }
  }
});
