package com.team1.library.service;

import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import com.team1.library.repository.AppUserRepository;

/**
 * Spring Security finds this bean on its own (IoC) and uses it to look up the account for every
 * Basic-auth request, then compares the supplied password with the stored BCrypt hash.
 */
@Service
public class DatabaseUserDetailsService implements UserDetailsService {

	private final AppUserRepository userRepository;

	public DatabaseUserDetailsService(AppUserRepository userRepository) {
		this.userRepository = userRepository;
	}

	@Override
	public UserDetails loadUserByUsername(String username) {
		return userRepository.findByUsername(username)
				.map(user -> User.withUsername(user.getUsername())
						.password(user.getPasswordHash())
						.roles(user.getRole().name())
						.build())
				.orElseThrow(() -> new UsernameNotFoundException("Unknown user."));
	}
}
