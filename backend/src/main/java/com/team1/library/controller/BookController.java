package com.team1.library.controller;

import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.team1.library.dto.BookRequest;
import com.team1.library.dto.BookResponse;
import com.team1.library.dto.PageResponse;
import com.team1.library.service.BookService;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/books")
public class BookController {

	private final BookService bookService;

	// Constructor injection (DI): Spring passes in the BookService bean.
	public BookController(BookService bookService) {
		this.bookService = bookService;
	}

	/** Example: {@code GET /api/books?query=java&page=0&size=10&sort=title,asc}. */
	@GetMapping
	public PageResponse<BookResponse> list(
			@RequestParam(defaultValue = "") String query,
			@PageableDefault(size = 10, sort = "title") Pageable pageable) {
		return bookService.search(query, pageable);
	}

	@PostMapping
	@ResponseStatus(HttpStatus.CREATED)
	public BookResponse add(@Valid @RequestBody BookRequest request) {
		return bookService.add(request);
	}
}
