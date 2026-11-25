package com.team1.library.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Table;

/** A person who borrows books. Inherits id and name from {@link Person}. */
@Entity
@Table(name = "members")
public class Member extends Person {

	@Enumerated(EnumType.STRING)
	@Column(nullable = false)
	private MemberType type;

	protected Member() {
	}

	public Member(String name, MemberType type) {
		super(name);
		this.type = type;
	}

	public MemberType getType() {
		return type;
	}

	public int getBorrowLimit() {
		return type.getBorrowLimit();
	}
}
