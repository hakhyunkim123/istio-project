package com.proj.dao;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

import com.proj.entity.ProjectEntity;

public interface ProjectEntityDAO extends CrudRepository<ProjectEntity, Long>{
	@Query("SELECT p.userId FROM ProjectEntity p WHERE p.projectId = :id")
	Iterable<String> findUserIdByProjectId(@Param("id") Long id);
	
	@Query("SELECT p FROM ProjectEntity p WHERE p.userId = :userId")
	Iterable<ProjectEntity> findAllByUserId(@Param("userId") String userId);
	
	/*@Query("SELECT p.user_name FROM ProjectEntity p WHERE p.entity_id = :projectEntityId")
	String findUserNameByPk(@Param("userId") Long projectEntityId);*/
}