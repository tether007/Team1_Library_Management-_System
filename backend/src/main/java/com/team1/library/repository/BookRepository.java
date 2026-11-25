package com.team1.library.repository;

import java.util.Collection;
import java.util.List;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import com.team1.library.model.Book;

/**
 * Spring Data generates the implementation at startup and registers it as a bean, so services
 * receive it through constructor injection (Dependency Injection) and never create it themselves.
 */
public interface BookRepository extends JpaRepository<Book, Long> {

	/** Case-insensitive search over title, author and ISBN. Paging and sorting come from the {@link Pageable}. */
	Page<Book> findByTitleContainingIgnoreCaseOrAuthorContainingIgnoreCaseOrIsbnContainingIgnoreCase(
			String title, String author, String isbn, Pageable pageable);

	boolean existsByIsbn(String isbn);

	long countByBorrowerId(Long memberId);

	/** Books currently borrowed, grouped per member, for the given member ids (one query for a whole page). */
	@Query("select b.borrower.id as memberId, count(b) as total from Book b "
			+ "where b.borrower.id in :memberIds group by b.borrower.id")
	List<BorrowCount> countBorrowedByMembers(@Param("memberIds") Collection<Long> memberIds);
}
