package com.team1.library.service;

import org.springframework.cache.annotation.CacheEvict;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.team1.library.config.CacheConfig;
import com.team1.library.dto.BookResponse;
import com.team1.library.dto.IssueRequest;
import com.team1.library.dto.ReturnRequest;
import com.team1.library.exception.BookNotAvailableException;
import com.team1.library.exception.BookNotFoundException;
import com.team1.library.exception.BookNotIssuedException;
import com.team1.library.exception.BorrowLimitExceededException;
import com.team1.library.exception.MemberNotFoundException;
import com.team1.library.model.Book;
import com.team1.library.model.Member;
import com.team1.library.repository.BookRepository;
import com.team1.library.repository.MemberRepository;

/** Issuing and returning books. Each method runs in one transaction, so a failed rule changes nothing. */
@Service
@Transactional
public class BorrowService {

	private final BookRepository bookRepository;
	private final MemberRepository memberRepository;

	// Constructor injection (DI): the container passes in the repositories.
	public BorrowService(BookRepository bookRepository, MemberRepository memberRepository) {
		this.bookRepository = bookRepository;
		this.memberRepository = memberRepository;
	}

	@CacheEvict(cacheNames = CacheConfig.BOOKS, allEntries = true)
	public BookResponse issue(IssueRequest request) {
		Book book = bookRepository.findById(request.bookId()).orElseThrow(BookNotFoundException::new);
		Member member = memberRepository.findById(request.memberId()).orElseThrow(MemberNotFoundException::new);

		if (!book.isAvailable()) {
			throw new BookNotAvailableException(book.getTitle());
		}
		if (bookRepository.countByBorrowerId(member.getId()) >= member.getBorrowLimit()) {
			throw new BorrowLimitExceededException(member.getName(), member.getBorrowLimit());
		}

		book.issueTo(member);
		return BookResponse.from(book);
	}

	@CacheEvict(cacheNames = CacheConfig.BOOKS, allEntries = true)
	public BookResponse giveBack(ReturnRequest request) {
		Book book = bookRepository.findById(request.bookId()).orElseThrow(BookNotFoundException::new);
		if (book.isAvailable()) {
			throw new BookNotIssuedException(book.getTitle());
		}

		book.markReturned();
		return BookResponse.from(book);
	}
}
