package com.proj.dao;

import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.CrudRepository;
import org.springframework.data.repository.query.Param;

import com.proj.entity.NoticeEntity;


public interface NoticeDAO extends CrudRepository<NoticeEntity, Long>{
	@Query("SELECT n FROM NoticeEntity n WHERE n.projectId = :projectId")
	Iterable<NoticeEntity> findNoticeAllByProjectId(@Param("projectId") Long projectId);
}