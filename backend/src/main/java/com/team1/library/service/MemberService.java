package com.team1.library.service;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.team1.library.dto.MemberRequest;
import com.team1.library.dto.MemberResponse;
import com.team1.library.dto.PageResponse;
import com.team1.library.model.Member;
import com.team1.library.repository.BookRepository;
import com.team1.library.repository.BorrowCount;
import com.team1.library.repository.MemberRepository;

@Service
@Transactional(readOnly = true)
public class MemberService {

	// Both repositories are injected by the Spring container (Dependency Injection).
	private final MemberRepository memberRepository;
	private final BookRepository bookRepository;

	public MemberService(MemberRepository memberRepository, BookRepository bookRepository) {
		this.memberRepository = memberRepository;
		this.bookRepository = bookRepository;
	}

	public PageResponse<MemberResponse> list(Pageable pageable) {
		Page<Member> page = memberRepository.findAll(pageable);
		List<Long> ids = page.getContent().stream().map(Member::getId).toList();
		Map<Long, Long> counts = bookRepository.countBorrowedByMembers(ids).stream()
				.collect(Collectors.toMap(BorrowCount::getMemberId, BorrowCount::getTotal));
		return PageResponse.from(page, member -> MemberResponse.from(member, counts.getOrDefault(member.getId(), 0L)));
	}

	@Transactional
	public MemberResponse add(MemberRequest request) {
		Member saved = memberRepository.save(new Member(request.name().trim(), request.role()));
		return MemberResponse.from(saved, 0);
	}
}
