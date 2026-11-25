package com.team1.library.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.team1.library.model.Member;

public interface MemberRepository extends JpaRepository<Member, Long> {
}
