// app.js

// Function to handle real-time search
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="search"]');
    const bookList = document.querySelector('ul');

    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = searchInput.value.toLowerCase();

            // Filter book list based on the search term
            const books = bookList.querySelectorAll('li');
            books.forEach(book => {
                const title = book.textContent.toLowerCase();
                if (title.includes(searchTerm)) {
                    book.style.display = '';
                } else {
                    book.style.display = 'none';
                }
            });
        });
    }
});

// Function to display book details without page reload (assuming you have an API endpoint for fetching book details)
function showBookDetails(bookId) {
    fetch(`/api/book/${bookId}`)
        .then(response => response.json())
        .then(data => {
            const detailsContainer = document.getElementById('book-details');
            detailsContainer.innerHTML = `
                <h2>${data.title}</h2>
                <p><strong>Author:</strong> ${data.author}</p>
                <p><strong>Genre:</strong> ${data.genre}</p>
                <p>${data.description}</p>
                <button onclick="borrowBook(${data.id})">Borrow</button>
            `;
            detailsContainer.style.display = 'block';
        })
        .catch(error => console.error('Error fetching book details:', error));
}

// Function to handle borrowing books
function borrowBook(bookId) {
    fetch(`/borrow/${bookId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert(data.message);  // Show success or error message
            if (data.success) {
                location.reload();  // Reload page to update book status
            }
        })
        .catch(error => console.error('Error borrowing book:', error));
}
