package com.team1.library.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.when;

import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;

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
import com.team1.library.model.MemberType;
import com.team1.library.repository.BookRepository;
import com.team1.library.repository.MemberRepository;

/** Pure unit test: the repositories are replaced by mocks, which constructor injection makes possible. */
@ExtendWith(MockitoExtension.class)
class BorrowServiceTest {

	@Mock
	private BookRepository bookRepository;

	@Mock
	private MemberRepository memberRepository;

	@InjectMocks
	private BorrowService borrowService;

	private Book book;
	private Member student;

	@BeforeEach
	void setUp() {
		book = new Book("Clean Code", "Robert C. Martin", "9780132350884");
		ReflectionTestUtils.setField(book, "id", 1L);
		student = new Member("Asha Rao", MemberType.STUDENT);
		ReflectionTestUtils.setField(student, "id", 7L);
	}

	@Test
	void issueMarksBookAsBorrowed() {
		when(bookRepository.findById(1L)).thenReturn(Optional.of(book));
		when(memberRepository.findById(7L)).thenReturn(Optional.of(student));
		when(bookRepository.countByBorrowerId(7L)).thenReturn(0L);

		BookResponse response = borrowService.issue(new IssueRequest(1L, 7L));

		assertThat(response.available()).isFalse();
		assertThat(response.borrowedBy()).isEqualTo(7L);
	}

	@Test
	void issueRejectsBookThatIsAlreadyIssued() {
		book.issueTo(student);
		when(bookRepository.findById(1L)).thenReturn(Optional.of(book));
		when(memberRepository.findById(7L)).thenReturn(Optional.of(student));

		assertThatThrownBy(() -> borrowService.issue(new IssueRequest(1L, 7L)))
				.isInstanceOf(BookNotAvailableException.class)
				.hasMessage("\"Clean Code\" is not available.");
	}

	@Test
	void issueEnforcesTheStudentLimit() {
		when(bookRepository.findById(1L)).thenReturn(Optional.of(book));
		when(memberRepository.findById(7L)).thenReturn(Optional.of(student));
		when(bookRepository.countByBorrowerId(7L)).thenReturn(3L);

		assertThatThrownBy(() -> borrowService.issue(new IssueRequest(1L, 7L)))
				.isInstanceOf(BorrowLimitExceededException.class)
				.hasMessage("Asha Rao has reached the borrow limit of 3.");
		assertThat(book.isAvailable()).isTrue();
	}

	@Test
	void facultyMayBorrowFiveBooks() {
		Member faculty = new Member("Dr. Mehta", MemberType.FACULTY);
		ReflectionTestUtils.setField(faculty, "id", 8L);
		when(bookRepository.findById(1L)).thenReturn(Optional.of(book));
		when(memberRepository.findById(8L)).thenReturn(Optional.of(faculty));
		when(bookRepository.countByBorrowerId(8L)).thenReturn(4L);

		assertThat(borrowService.issue(new IssueRequest(1L, 8L)).available()).isFalse();
	}

	@Test
	void issueRejectsUnknownBookAndMember() {
		when(bookRepository.findById(99L)).thenReturn(Optional.empty());
		assertThatThrownBy(() -> borrowService.issue(new IssueRequest(99L, 7L)))
				.isInstanceOf(BookNotFoundException.class);

		when(bookRepository.findById(1L)).thenReturn(Optional.of(book));
		when(memberRepository.findById(99L)).thenReturn(Optional.empty());
		assertThatThrownBy(() -> borrowService.issue(new IssueRequest(1L, 99L)))
				.isInstanceOf(MemberNotFoundException.class);
	}

	@Test
	void giveBackMakesBookAvailable() {
		book.issueTo(student);
		when(bookRepository.findById(1L)).thenReturn(Optional.of(book));

		BookResponse response = borrowService.giveBack(new ReturnRequest(1L));

		assertThat(response.available()).isTrue();
		assertThat(response.borrowedBy()).isNull();
	}

	@Test
	void giveBackRejectsBookThatWasNotIssued() {
		when(bookRepository.findById(1L)).thenReturn(Optional.of(book));

		assertThatThrownBy(() -> borrowService.giveBack(new ReturnRequest(1L)))
				.isInstanceOf(BookNotIssuedException.class)
				.hasMessage("\"Clean Code\" was not issued.");
	}
}
