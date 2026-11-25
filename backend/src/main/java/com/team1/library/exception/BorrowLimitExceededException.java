package com.team1.library.exception;

import org.springframework.http.HttpStatus;

public class BorrowLimitExceededException extends LibraryException {

	public BorrowLimitExceededException(String memberName, int limit) {
		super(HttpStatus.CONFLICT, memberName + " has reached the borrow limit of " + limit + ".");
	}
}
