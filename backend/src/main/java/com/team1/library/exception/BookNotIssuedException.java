package com.team1.library.exception;

import org.springframework.http.HttpStatus;

public class BookNotIssuedException extends LibraryException {

	public BookNotIssuedException(String title) {
		super(HttpStatus.CONFLICT, "\"" + title + "\" was not issued.");
	}
}
