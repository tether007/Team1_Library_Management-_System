package com.team1.library.service;

import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.team1.library.config.CacheConfig;
import com.team1.library.dto.BookRequest;
import com.team1.library.dto.BookResponse;
import com.team1.library.dto.PageResponse;
import com.team1.library.exception.DuplicateIsbnException;
import com.team1.library.model.Book;
import com.team1.library.repository.BookRepository;

/**
 * {@code @Service} registers this class as a Spring bean. The repository it needs is passed to the
 * constructor and supplied by the container (constructor-based Dependency Injection), so the class
 * never builds its own dependencies and can be tested with a substitute.
 */
@Service
@Transactional(readOnly = true)
public class BookService {

	private final BookRepository bookRepository;

	public BookService(BookRepository bookRepository) {
		this.bookRepository = bookRepository;
	}

	/** Results are cached per (query, page, size, sort); any write to books clears the cache. */
	@Cacheable(cacheNames = CacheConfig.BOOKS, key = "#query + '|' + #pageable")
	public PageResponse<BookResponse> search(String query, Pageable pageable) {
		String term = query == null ? "" : query.trim();
		return PageResponse.from(
				bookRepository.findByTitleContainingIgnoreCaseOrAuthorContainingIgnoreCaseOrIsbnContainingIgnoreCase(
						term, term, term, pageable),
				BookResponse::from);
	}

	@Transactional
	@CacheEvict(cacheNames = CacheConfig.BOOKS, allEntries = true)
	public BookResponse add(BookRequest request) {
		if (bookRepository.existsByIsbn(request.isbn())) {
			throw new DuplicateIsbnException(request.isbn());
		}
		Book saved = bookRepository.save(new Book(request.title(), request.author(), request.isbn()));
		return BookResponse.from(saved);
	}
}
