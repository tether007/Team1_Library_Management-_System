package com.team1.library.repository;

/** Projection for the "books borrowed per member" query. */
public interface BorrowCount {

	Long getMemberId();

	long getTotal();
}
