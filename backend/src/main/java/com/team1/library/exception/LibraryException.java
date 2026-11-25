package com.team1.library.exception;

import org.springframework.http.HttpStatus;

/**
 * Base class for every business-rule failure. Each subclass fixes its own HTTP status and message,
 * so the global handler can translate any of them without knowing the concrete type (polymorphism).
 */
public abstract class LibraryException extends RuntimeException {

	private final HttpStatus status;

	protected LibraryException(HttpStatus status, String message) {
		super(message);
		this.status = status;
	}

	public HttpStatus getStatus() {
		return status;
	}
}
