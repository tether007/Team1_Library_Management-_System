package com.team1.library.exception;

import org.springframework.http.HttpStatus;

public class DuplicateIsbnException extends LibraryException {

	public DuplicateIsbnException(String isbn) {
		super(HttpStatus.CONFLICT, "A book with ISBN " + isbn + " already exists.");
	}
}
