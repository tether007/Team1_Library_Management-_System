package com.team1.library.exception;

import org.springframework.http.HttpStatus;

public class MemberNotFoundException extends LibraryException {

	public MemberNotFoundException() {
		super(HttpStatus.NOT_FOUND, "Invalid member.");
	}
}
