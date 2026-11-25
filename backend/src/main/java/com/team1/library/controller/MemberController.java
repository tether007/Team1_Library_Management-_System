package com.team1.library.controller;

import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.team1.library.dto.MemberRequest;
import com.team1.library.dto.MemberResponse;
import com.team1.library.dto.PageResponse;
import com.team1.library.service.MemberService;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/members")
public class MemberController {

	private final MemberService memberService;

	public MemberController(MemberService memberService) {
		this.memberService = memberService;
	}

	/** Example: {@code GET /api/members?page=0&size=10&sort=name,asc}. */
	@GetMapping
	public PageResponse<MemberResponse> list(@PageableDefault(size = 10, sort = "name") Pageable pageable) {
		return memberService.list(pageable);
	}

	@PostMapping
	@ResponseStatus(HttpStatus.CREATED)
	public MemberResponse add(@Valid @RequestBody MemberRequest request) {
		return memberService.add(request);
	}
}
