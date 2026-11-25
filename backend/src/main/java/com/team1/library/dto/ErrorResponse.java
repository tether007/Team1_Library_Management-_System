package com.team1.library.dto;

/** Error body used by every failing call: {@code { "message": "..." }}. */
public record ErrorResponse(String message) {
}
