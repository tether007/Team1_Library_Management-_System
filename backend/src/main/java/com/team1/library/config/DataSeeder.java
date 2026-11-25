package com.team1.library.config;

import java.util.List;

import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import com.team1.library.model.AppUser;
import com.team1.library.model.Book;
import com.team1.library.model.Member;
import com.team1.library.model.MemberType;
import com.team1.library.model.Role;
import com.team1.library.repository.AppUserRepository;
import com.team1.library.repository.BookRepository;
import com.team1.library.repository.MemberRepository;

/**
 * Fills the in-memory database on startup so the demo has accounts and books to work with.
 * The data is not persisted anywhere: it is recreated on every start.
 * The demo passwords below are for local use only.
 */
@Component
public class DataSeeder implements ApplicationRunner {

	private final AppUserRepository userRepository;
	private final MemberRepository memberRepository;
	private final BookRepository bookRepository;
	private final PasswordEncoder passwordEncoder;

	// All four collaborators are supplied by the container (constructor DI).
	public DataSeeder(AppUserRepository userRepository, MemberRepository memberRepository,
			BookRepository bookRepository, PasswordEncoder passwordEncoder) {
		this.userRepository = userRepository;
		this.memberRepository = memberRepository;
		this.bookRepository = bookRepository;
		this.passwordEncoder = passwordEncoder;
	}

	@Override
	public void run(ApplicationArguments args) {
		if (userRepository.count() > 0) {
			return;
		}

		userRepository.saveAll(List.of(
				new AppUser("Administrator", "admin", passwordEncoder.encode("admin123"), Role.ADMIN),
				new AppUser("Head Librarian", "librarian", passwordEncoder.encode("librarian123"), Role.LIBRARIAN),
				new AppUser("Library Member", "member", passwordEncoder.encode("member123"), Role.MEMBER)));

		memberRepository.saveAll(List.of(
				new Member("Asha Rao", MemberType.STUDENT),
				new Member("Dr. Mehta", MemberType.FACULTY)));

		bookRepository.saveAll(List.of(
				new Book("Clean Code", "Robert C. Martin", "9780132350884"),
				new Book("Effective Java", "Joshua Bloch", "9780134685991"),
				new Book("Head First Java", "Kathy Sierra", "9781491910771"),
				new Book("Refactoring", "Martin Fowler", "9780134757599"),
				new Book("Design Patterns", "Erich Gamma", "9780201633610"),
				new Book("The Pragmatic Programmer", "Andrew Hunt", "9780135957059"),
				new Book("Java Concurrency in Practice", "Brian Goetz", "9780321349606"),
				new Book("Spring in Action", "Craig Walls", "9781617297571"),
				new Book("Domain-Driven Design", "Eric Evans", "9780321125217"),
				new Book("Introduction to Algorithms", "Thomas H. Cormen", "9780262046305"),
				new Book("Code Complete", "Steve McConnell", "9780735619678"),
				new Book("Test Driven Development", "Kent Beck", "9780321146533")));
	}
}
