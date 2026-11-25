package com.team1.library.config;

import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Configuration;

/**
 * Turns on Spring's cache abstraction. Boot supplies an in-memory cache manager, so cached book
 * pages live in the JVM and disappear on restart (nothing is written to disk).
 */
@Configuration
@EnableCaching
public class CacheConfig {

	public static final String BOOKS = "books";
}
