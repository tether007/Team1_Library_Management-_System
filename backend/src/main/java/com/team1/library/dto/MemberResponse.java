package com.team1.library.dto;

import com.team1.library.model.Member;
import com.team1.library.model.MemberType;

/** {@code role} is the member type (STUDENT or FACULTY); it is not a login role. */
public record MemberResponse(Long id, String name, MemberType role, long borrowedCount) {

	public static MemberResponse from(Member member, long borrowedCount) {
		return new MemberResponse(member.getId(), member.getName(), member.getType(), borrowedCount);
	}
}
