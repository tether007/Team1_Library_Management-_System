package com.team1.library.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.team1.library.dto.UserResponse;
import com.team1.library.model.Role;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

	/**
	 * The security filter has already verified the Basic credentials against the database by the time
	 * this runs, so a successful response means "these credentials are valid" and tells the UI the role.
	 */
	@GetMapping("/me")
	public UserResponse me(Authentication authentication) {
		String authority = authentication.getAuthorities().stream()
				.map(GrantedAuthority::getAuthority)
				.findFirst()
				.orElseThrow();
		return new UserResponse(authentication.getName(), Role.valueOf(authority.replaceFirst("^ROLE_", "")));
	}
}
