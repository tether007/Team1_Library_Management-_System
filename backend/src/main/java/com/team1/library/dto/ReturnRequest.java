package com.team1.library.dto;

import jakarta.validation.constraints.NotNull;

public record ReturnRequest(@NotNull(message = "Book is required.") Long bookId) {
}
