package com.team1.library.dto;

import jakarta.validation.constraints.NotNull;

public record IssueRequest(
		@NotNull(message = "Book is required.") Long bookId,
		@NotNull(message = "Member is required.") Long memberId) {
}
