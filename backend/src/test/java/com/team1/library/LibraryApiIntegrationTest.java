package com.team1.library;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.httpBasic;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.concurrent.ConcurrentMap;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc;
import org.springframework.cache.Cache;
import org.springframework.cache.CacheManager;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.ResultActions;
import org.springframework.test.web.servlet.request.MockHttpServletRequestBuilder;
import org.springframework.transaction.annotation.Transactional;

import com.team1.library.config.CacheConfig;
import com.team1.library.model.Book;
import com.team1.library.model.Member;
import com.team1.library.repository.BookRepository;
import com.team1.library.repository.MemberRepository;

/**
 * Full-stack test: real Spring context, real security filter chain, in-memory H2 and seeded demo data.
 * Each test runs in a transaction that is rolled back, so tests do not affect each other.
 */
@SpringBootTest
@AutoConfigureMockMvc
@Transactional
class LibraryApiIntegrationTest {

	@Autowired
	private MockMvc mockMvc;

	@Autowired
	private BookRepository bookRepository;

	@Autowired
	private MemberRepository memberRepository;

	@Autowired
	private CacheManager cacheManager;

	@BeforeEach
	void clearCache() {
		cacheManager.getCache(CacheConfig.BOOKS).clear();
	}

	// ---------- authentication ----------

	@Test
	void requestWithoutCredentialsIsRejected() throws Exception {
		mockMvc.perform(get("/api/books"))
				.andExpect(status().isUnauthorized())
				.andExpect(jsonPath("$.message").value("Authentication required."));
	}

	@Test
	void wrongPasswordIsRejected() throws Exception {
		mockMvc.perform(get("/api/auth/me").with(httpBasic("admin", "wrong")))
				.andExpect(status().isUnauthorized())
				.andExpect(jsonPath("$.message").value("Invalid username or password."));
	}

	@Test
	void validCredentialsReturnUsernameAndRole() throws Exception {
		mockMvc.perform(get("/api/auth/me").with(httpBasic("librarian", "librarian123")))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.username").value("librarian"))
				.andExpect(jsonPath("$.role").value("LIBRARIAN"));
	}

	// ---------- role-based access ----------

	@Test
	void memberCannotAddBooksOrIssueThem() throws Exception {
		json(post("/api/books"), "member", "member123", "{\"title\":\"X\",\"author\":\"Y\",\"isbn\":\"1\"}")
				.andExpect(status().isForbidden())
				.andExpect(jsonPath("$.message").value("You do not have permission to do that."));

		json(post("/api/borrow/issue"), "member", "member123", "{\"bookId\":1,\"memberId\":1}")
				.andExpect(status().isForbidden());
	}

	@Test
	void onlyAdminCanAddMembersAndLibrarianCanListThem() throws Exception {
		String body = "{\"name\":\"Ravi Kumar\",\"role\":\"STUDENT\"}";

		json(post("/api/members"), "librarian", "librarian123", body).andExpect(status().isForbidden());
		json(post("/api/members"), "admin", "admin123", body)
				.andExpect(status().isCreated())
				.andExpect(jsonPath("$.name").value("Ravi Kumar"))
				.andExpect(jsonPath("$.borrowedCount").value(0));

		mockMvc.perform(get("/api/members").with(httpBasic("librarian", "librarian123")))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.totalElements").value(3));
		mockMvc.perform(get("/api/members").with(httpBasic("member", "member123")))
				.andExpect(status().isForbidden());
	}

	// ---------- books: paging, sorting, searching ----------

	@Test
	void booksAreSortedByTitleAndPagedByDefault() throws Exception {
		mockMvc.perform(get("/api/books").with(httpBasic("member", "member123")))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.content.length()").value(10))
				.andExpect(jsonPath("$.content[0].title").value("Clean Code"))
				.andExpect(jsonPath("$.page").value(0))
				.andExpect(jsonPath("$.size").value(10))
				.andExpect(jsonPath("$.totalElements").value(12))
				.andExpect(jsonPath("$.totalPages").value(2));
	}

	@Test
	void clientControlsPageSizeAndSortDirection() throws Exception {
		mockMvc.perform(get("/api/books?page=1&size=2&sort=title,desc").with(httpBasic("member", "member123")))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.content.length()").value(2))
				.andExpect(jsonPath("$.content[0].title").value("Spring in Action"))
				.andExpect(jsonPath("$.content[1].title").value("Refactoring"))
				.andExpect(jsonPath("$.page").value(1))
				.andExpect(jsonPath("$.totalPages").value(6));
	}

	@Test
	void searchMatchesTitleAuthorOrIsbnIgnoringCase() throws Exception {
		mockMvc.perform(get("/api/books?query=JAVA").with(httpBasic("member", "member123")))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.totalElements").value(3));
		mockMvc.perform(get("/api/books?query=fowler").with(httpBasic("member", "member123")))
				.andExpect(jsonPath("$.content[0].title").value("Refactoring"));
	}

	@Test
	void sortingByUnknownPropertyIsABadRequest() throws Exception {
		mockMvc.perform(get("/api/books?sort=nonsense,asc").with(httpBasic("member", "member123")))
				.andExpect(status().isBadRequest())
				.andExpect(jsonPath("$.message").value("Invalid sort or paging parameter."));
	}

	// ---------- books: adding ----------

	@Test
	void librarianAddsABookAndDuplicateIsbnIsRejected() throws Exception {
		String body = "{\"title\":\"Patterns\",\"author\":\"A. Author\",\"isbn\":\"0000000000001\"}";

		json(post("/api/books"), "librarian", "librarian123", body)
				.andExpect(status().isCreated())
				.andExpect(jsonPath("$.available").value(true));
		json(post("/api/books"), "librarian", "librarian123", body)
				.andExpect(status().isConflict())
				.andExpect(jsonPath("$.message").value("A book with ISBN 0000000000001 already exists."));
	}

	@Test
	void blankFieldsAreRejectedWithTheFieldMessage() throws Exception {
		json(post("/api/books"), "admin", "admin123", "{\"title\":\" \",\"author\":\"A\",\"isbn\":\"1\"}")
				.andExpect(status().isBadRequest())
				.andExpect(jsonPath("$.message").value("Title is required."));
	}

	// ---------- borrowing ----------

	@Test
	void issueAndReturnUpdateAvailabilityAndBorrowedCount() throws Exception {
		Book book = bookByTitle("Clean Code");
		Member asha = memberByName("Asha Rao");

		json(post("/api/borrow/issue"), "librarian", "librarian123", issueBody(book, asha))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.available").value(false))
				.andExpect(jsonPath("$.borrowedBy").value(asha.getId()));

		mockMvc.perform(get("/api/members?sort=name,asc").with(httpBasic("librarian", "librarian123")))
				.andExpect(jsonPath("$.content[0].name").value("Asha Rao"))
				.andExpect(jsonPath("$.content[0].borrowedCount").value(1));

		json(post("/api/borrow/issue"), "librarian", "librarian123", issueBody(book, asha))
				.andExpect(status().isConflict())
				.andExpect(jsonPath("$.message").value("\"Clean Code\" is not available."));

		json(post("/api/borrow/return"), "librarian", "librarian123", "{\"bookId\":" + book.getId() + "}")
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.available").value(true))
				.andExpect(jsonPath("$.borrowedBy").isEmpty());

		json(post("/api/borrow/return"), "librarian", "librarian123", "{\"bookId\":" + book.getId() + "}")
				.andExpect(status().isConflict())
				.andExpect(jsonPath("$.message").value("\"Clean Code\" was not issued."));
	}

	@Test
	void studentCannotBorrowMoreThanThreeBooks() throws Exception {
		Member asha = memberByName("Asha Rao");
		for (String title : new String[] { "Clean Code", "Effective Java", "Refactoring" }) {
			json(post("/api/borrow/issue"), "admin", "admin123", issueBody(bookByTitle(title), asha))
					.andExpect(status().isOk());
		}

		json(post("/api/borrow/issue"), "admin", "admin123", issueBody(bookByTitle("Code Complete"), asha))
				.andExpect(status().isConflict())
				.andExpect(jsonPath("$.message").value("Asha Rao has reached the borrow limit of 3."));
	}

	@Test
	void unknownBookAndMemberAreNotFound() throws Exception {
		Member asha = memberByName("Asha Rao");

		json(post("/api/borrow/issue"), "admin", "admin123", "{\"bookId\":99999,\"memberId\":" + asha.getId() + "}")
				.andExpect(status().isNotFound())
				.andExpect(jsonPath("$.message").value("Book not found."));
		json(post("/api/borrow/issue"), "admin", "admin123",
				"{\"bookId\":" + bookByTitle("Clean Code").getId() + ",\"memberId\":99999}")
				.andExpect(status().isNotFound())
				.andExpect(jsonPath("$.message").value("Invalid member."));
	}

	// ---------- caching ----------

	@Test
	void bookListIsCachedAndClearedByWrites() throws Exception {
		mockMvc.perform(get("/api/books").with(httpBasic("member", "member123"))).andExpect(status().isOk());
		assertThat(cachedEntries()).hasSize(1);

		mockMvc.perform(get("/api/books").with(httpBasic("member", "member123"))).andExpect(status().isOk());
		assertThat(cachedEntries()).hasSize(1);

		json(post("/api/books"), "admin", "admin123",
				"{\"title\":\"New\",\"author\":\"A\",\"isbn\":\"0000000000002\"}").andExpect(status().isCreated());
		assertThat(cachedEntries()).isEmpty();
	}

	// ---------- helpers ----------

	private ConcurrentMap<?, ?> cachedEntries() {
		Cache cache = cacheManager.getCache(CacheConfig.BOOKS);
		return (ConcurrentMap<?, ?>) cache.getNativeCache();
	}

	private ResultActions json(MockHttpServletRequestBuilder request, String user, String password, String body)
			throws Exception {
		return mockMvc.perform(request.with(httpBasic(user, password))
				.contentType(MediaType.APPLICATION_JSON)
				.content(body));
	}

	private String issueBody(Book book, Member member) {
		return "{\"bookId\":" + book.getId() + ",\"memberId\":" + member.getId() + "}";
	}

	private Book bookByTitle(String title) {
		return bookRepository.findAll().stream().filter(b -> b.getTitle().equals(title)).findFirst().orElseThrow();
	}

	private Member memberByName(String name) {
		return memberRepository.findAll().stream().filter(m -> m.getName().equals(name)).findFirst().orElseThrow();
	}
}
