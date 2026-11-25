package com.team1.library.dto;

import com.team1.library.model.MemberType;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record MemberRequest(
		@NotBlank(message = "Name is required.") String name,
		@NotNull(message = "Member type is required.") MemberType role) {
}
