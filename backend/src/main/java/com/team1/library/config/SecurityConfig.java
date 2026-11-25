package com.team1.library.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

/**
 * HTTP Basic authentication with role-based access control (RBAC).
 * {@code @Configuration} classes are read by the container, and every {@code @Bean} method's return
 * value becomes a managed bean (IoC). The {@link SecurityErrorHandler} parameter is injected by Spring.
 */
@Configuration
public class SecurityConfig {

	@Bean
	SecurityFilterChain securityFilterChain(HttpSecurity http, SecurityErrorHandler errorHandler) throws Exception {
		http
				// Stateless API with credentials on every request, so there is no session or CSRF cookie to protect.
				.csrf(AbstractHttpConfigurer::disable)
				.sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
				.httpBasic(basic -> basic.authenticationEntryPoint(errorHandler))
				.exceptionHandling(errors -> errors
						.authenticationEntryPoint(errorHandler)
						.accessDeniedHandler(errorHandler))
				.authorizeHttpRequests(requests -> requests
						.requestMatchers(HttpMethod.GET, "/api/auth/me", "/api/books").authenticated()
						.requestMatchers(HttpMethod.POST, "/api/books").hasAnyRole("ADMIN", "LIBRARIAN")
						.requestMatchers(HttpMethod.GET, "/api/members").hasAnyRole("ADMIN", "LIBRARIAN")
						.requestMatchers(HttpMethod.POST, "/api/members").hasRole("ADMIN")
						.requestMatchers(HttpMethod.POST, "/api/borrow/issue", "/api/borrow/return")
								.hasAnyRole("ADMIN", "LIBRARIAN")
						.anyRequest().denyAll());
		return http.build();
	}

	/** Passwords are stored only as BCrypt hashes. */
	@Bean
	PasswordEncoder passwordEncoder() {
		return new BCryptPasswordEncoder();
	}
}
