package com.team1.library.exception;

import org.springframework.http.HttpStatus;

public class BookNotFoundException extends LibraryException {

	public BookNotFoundException() {
		super(HttpStatus.NOT_FOUND, "Book not found.");
	}
}
