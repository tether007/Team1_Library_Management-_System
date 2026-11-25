package com.team1.library.model;

/** Kind of library member. Each kind carries its own borrow limit. */
public enum MemberType {

	STUDENT(3),
	FACULTY(5);

	private final int borrowLimit;

	MemberType(int borrowLimit) {
		this.borrowLimit = borrowLimit;
	}

	public int getBorrowLimit() {
		return borrowLimit;
	}
}
