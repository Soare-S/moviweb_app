// pagination.js
const loadMoreBtn = document.getElementById('load-more-btn');
let currentPage = 1;

loadMoreBtn.addEventListener('click', () => {
    currentPage += 1;
    fetchMovies(currentPage);
});

function fetchMovies(page) {
    const user_id = '{{ user_id }}'; // Replace with the actual user ID from the Flask template
    const url = `/users/${user_id}?page=${page}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const movieList = document.getElementById('movie-list');
            const hasMore = data.has_more;
            const movies = data.movies;

            // Append fetched movies to the movie list
            movies.forEach(movie => {
                const movieItem = document.createElement('li');
                // Construct the movie item HTML here (similar to user_movies.html template)
                movieItem.innerHTML = `
                    <h3 class="movie-title">${movie.title}</h3>
                    <img class="movie-poster" src="${movie.poster}" title="poster">
                    <p>
                        <a href="/users/${user_id}/update_movie/${movie.id}">Edit</a>
                        <a href="/users/${user_id}/delete_movie/${movie.id}">Delete</a>
                    </p>
                `;
                movieList.appendChild(movieItem);
            });

            // Show/hide "Load More" button based on hasMore
            if (hasMore) {
                loadMoreBtn.style.display = 'block';
            } else {
                loadMoreBtn.style.display = 'none';
            }
        })
        .catch(error => console.error('Error fetching movies:', error));
}

// Initial fetch to load the first page of movies
fetchMovies(currentPage);

