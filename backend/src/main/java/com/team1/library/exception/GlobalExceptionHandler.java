package com.team1.library.exception;

import org.springframework.dao.InvalidDataAccessApiUsageException;
import org.springframework.data.core.PropertyReferenceException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import com.team1.library.dto.ErrorResponse;

/**
 * Central exception handling for all controllers. Spring discovers this class through
 * {@code @RestControllerAdvice} and applies it automatically (IoC: no controller calls it).
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

	@ExceptionHandler(LibraryException.class)
	public ResponseEntity<ErrorResponse> handleLibrary(LibraryException ex) {
		return ResponseEntity.status(ex.getStatus()).body(new ErrorResponse(ex.getMessage()));
	}

	@ExceptionHandler(MethodArgumentNotValidException.class)
	public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
		String message = ex.getBindingResult().getFieldErrors().stream()
				.findFirst()
				.map(error -> error.getDefaultMessage())
				.orElse("Invalid request.");
		return ResponseEntity.badRequest().body(new ErrorResponse(message));
	}

	@ExceptionHandler(HttpMessageNotReadableException.class)
	public ResponseEntity<ErrorResponse> handleUnreadableBody() {
		return ResponseEntity.badRequest().body(new ErrorResponse("Malformed request body."));
	}

	/** Sorting by a property that does not exist. */
	@ExceptionHandler({ PropertyReferenceException.class, InvalidDataAccessApiUsageException.class })
	public ResponseEntity<ErrorResponse> handleBadSort() {
		return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(new ErrorResponse("Invalid sort or paging parameter."));
	}
}
