package com.team1.library.config;

import java.io.IOException;
import java.nio.charset.StandardCharsets;

import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.stereotype.Component;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

/**
 * Answers security failures with the same {@code { "message": "..." }} body as the rest of the API.
 * It deliberately sends no {@code WWW-Authenticate} header, so browsers do not open their own login
 * dialog and the React login page stays in control.
 * Declared as a {@code @Component}, so Spring creates it once and injects it into {@link SecurityConfig}.
 */
@Component
public class SecurityErrorHandler implements AuthenticationEntryPoint, AccessDeniedHandler {

	@Override
	public void commence(HttpServletRequest request, HttpServletResponse response,
			AuthenticationException exception) throws IOException {
		String message = exception instanceof BadCredentialsException
				? "Invalid username or password."
				: "Authentication required.";
		write(response, HttpStatus.UNAUTHORIZED, message);
	}

	@Override
	public void handle(HttpServletRequest request, HttpServletResponse response,
			AccessDeniedException exception) throws IOException {
		write(response, HttpStatus.FORBIDDEN, "You do not have permission to do that.");
	}

	// Messages are fixed strings, so no request data is written into the JSON.
	private void write(HttpServletResponse response, HttpStatus status, String message) throws IOException {
		response.setStatus(status.value());
		response.setContentType(MediaType.APPLICATION_JSON_VALUE);
		response.setCharacterEncoding(StandardCharsets.UTF_8.name());
		response.getWriter().write("{\"message\":\"" + message + "\"}");
	}
}
