package com.team1.library.exception;

import org.springframework.http.HttpStatus;

public class BookNotAvailableException extends LibraryException {

	public BookNotAvailableException(String title) {
		super(HttpStatus.CONFLICT, "\"" + title + "\" is not available.");
	}
}
