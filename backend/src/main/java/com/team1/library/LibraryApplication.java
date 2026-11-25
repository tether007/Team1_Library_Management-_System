package com.team1.library;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Entry point. {@code @SpringBootApplication} turns on component scanning, so every class annotated
 * with a stereotype ({@code @Service}, {@code @RestController}, {@code @Component}, {@code @Configuration})
 * under this package becomes a bean owned by the Spring container (Inversion of Control).
 */
@SpringBootApplication
public class LibraryApplication {

	public static void main(String[] args) {
		SpringApplication.run(LibraryApplication.class, args);
	}
}
