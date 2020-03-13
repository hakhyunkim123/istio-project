package com.proj.entity;

import java.sql.Timestamp;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

import lombok.Data;

@Data
@Entity
@Table(name="project_entity")
public class ProjectEntity {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name="entity_id")
	private Long projectEntityId;
	
	@Column(name="project_id", length=50, nullable = false)
	private Long projectId;
	
	@Column(name="project_name", length=50)
	private String projectName;
	
	@Column(name="date")
	private Timestamp enteredDate;
	
	@Column(name="user_id", nullable = false)
	private String userId;
}
