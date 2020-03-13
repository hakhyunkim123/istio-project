package com.proj.entity;

import java.sql.Timestamp;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
@Table(name="project_info")
public class ProjectInfo {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "project_id")
	private Long projectId;
	
	@Column(name = "project_name", length=50, nullable = false)
	private String projectName;
	
	//@Temporal(TemporalType.TIMESTAMP)
	@Column(name="date")
	private Timestamp createdDate;
	
	@Column(name = "master", length=20, nullable = false)
	private String master;
	
	@Column(name = "project_description", length=500)
	private String projectDescription;
}
