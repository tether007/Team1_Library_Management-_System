package com.team1.library.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.team1.library.dto.BookResponse;
import com.team1.library.dto.IssueRequest;
import com.team1.library.dto.ReturnRequest;
import com.team1.library.service.BorrowService;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/borrow")
public class BorrowController {

	private final BorrowService borrowService;

	public BorrowController(BorrowService borrowService) {
		this.borrowService = borrowService;
	}

	@PostMapping("/issue")
	public BookResponse issue(@Valid @RequestBody IssueRequest request) {
		return borrowService.issue(request);
	}

	@PostMapping("/return")
	public BookResponse giveBack(@Valid @RequestBody ReturnRequest request) {
		return borrowService.giveBack(request);
	}
}
