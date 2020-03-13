package com.proj.dao;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

import com.proj.entity.ProjectInfo;

public interface ProjectInfoDAO extends CrudRepository<ProjectInfo, Long>{
	@Query("SELECT p.projectName FROM ProjectInfo p WHERE p.projectId = :projectId")
	String findProjectNameById(@Param("projectId") Long projectId);
}