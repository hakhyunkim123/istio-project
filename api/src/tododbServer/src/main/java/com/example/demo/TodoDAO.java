package com.example.demo;

import org.springframework.data.repository.CrudRepository;

public interface TodoDAO extends CrudRepository<TodoEntity, Long>{
//	default BookEntity findOne(Long id) {
//		return (BookEntity) findById(id).orElse(null);
//	}
}
