package com.proj.entity;

import java.sql.Timestamp;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;
//import javax.persistence.Temporal;
//import javax.persistence.TemporalType;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@Entity
@Table(name="notice")
public class NoticeEntity {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long noticeId;
	
	@Column(nullable = false)
	private Long projectId;
	
	//@Temporal(TemporalType.TIMESTAMP)
	@Column(name="date", nullable = false)
	private Timestamp createdDate;
	
	@Column(length=10, nullable = false)
	private String author;
	
	@Column(length=500)
	private String text;
	
	@Column(length=50, nullable = false)
	private String title;
}
