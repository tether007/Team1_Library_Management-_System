package com.team1.library.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.team1.library.model.AppUser;

public interface AppUserRepository extends JpaRepository<AppUser, Long> {

	Optional<AppUser> findByUsername(String username);
}
