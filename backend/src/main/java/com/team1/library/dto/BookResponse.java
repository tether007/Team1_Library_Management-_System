package com.team1.library.dto;

import com.team1.library.model.Book;

public record BookResponse(Long id, String title, String author, String isbn, boolean available, Long borrowedBy) {

	public static BookResponse from(Book book) {
		Long borrowerId = book.getBorrower() == null ? null : book.getBorrower().getId();
		return new BookResponse(book.getId(), book.getTitle(), book.getAuthor(), book.getIsbn(),
				book.isAvailable(), borrowerId);
	}
}
