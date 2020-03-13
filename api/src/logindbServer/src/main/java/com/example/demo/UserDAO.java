package com.example.demo;

import java.util.List;


import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;

interface UserIdAndName{
    String getId();
    String getName();
}

public interface UserDAO extends CrudRepository<UserEntity, String> {
	default UserEntity findOne(String id) {
		return (UserEntity) findById(id).orElse(null);
	}
	
	@Query("SELECT u.id FROM UserEntity u")
	Iterable<String> getIdAll();
	
	@Query("SELECT u FROM UserEntity u")
	List<UserIdAndName> findAllIdAndName();
}