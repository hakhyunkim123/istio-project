package com.proj.entity;

import java.util.List;
import java.util.Map;

import lombok.Data;

@Data
public class AddProjectParam {
	private Map<String, String> projectName;
	private Map<String, String> projectDescription;
	private Map<String, List<String>> userIdList;
}