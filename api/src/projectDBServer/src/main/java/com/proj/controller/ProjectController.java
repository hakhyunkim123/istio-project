package com.proj.controller;

import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import javax.transaction.Transactional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import com.proj.dao.NoticeDAO;
import com.proj.dao.ProjectEntityDAO;
import com.proj.dao.ProjectInfoDAO;
import com.proj.entity.JsonEntity;
import com.proj.entity.NoticeEntity;
import com.proj.entity.ProjectEntity;
import com.proj.entity.ProjectInfo;

@RestController
public class ProjectController {
	@Autowired
	private NoticeDAO noticeDAO;
	@Autowired
	private ProjectInfoDAO projectInfoDAO;
	@Autowired
	private ProjectEntityDAO projectEntityDAO;
	@Autowired
	RestTemplate restTemplate;
	
	@GetMapping("/proj/noticeList/{projectId}")
	public Iterable<NoticeEntity> getNoticeList(@PathVariable Long projectId){
		return noticeDAO.findNoticeAllByProjectId(projectId);
	}
	
	@Transactional
	@PostMapping("/proj/createNotice/{projectId}")
	public NoticeEntity createNotice(@PathVariable Long projectId, NoticeEntity param) {
		param.setProjectId(projectId);
		param.setCreatedDate(new Timestamp(System.currentTimeMillis()));
	    return noticeDAO.save(param);
	}
	
	@Transactional
	@DeleteMapping("/proj/deleteNotice/{noticeId}")
	public String deleteNotice(@PathVariable Long noticeId) {
		noticeDAO.deleteById(noticeId);
	    return "SUCCESS";
	}
	
	@Transactional
	@GetMapping("/proj/noticeDetail/{noticeId}")
	public NoticeEntity getNoticeDetail(@PathVariable Long noticeId) {
		//Optional<NoticeEntity> noticeById = projectDAO.findById(pk);
		NoticeEntity notice = noticeDAO.findById(noticeId).orElse(null); 
	    return notice;
	}
	
	@Transactional
	@PutMapping("/proj/updateNotice/{noticeId}")
	public String updateNotice(@PathVariable Long noticeId, NoticeEntity noticeDetails) {
		NoticeEntity notice = noticeDAO.findById(noticeId).orElse(null); 
		
		if(notice == null) return "FAIL";
				
		notice.setTitle(noticeDetails.getTitle());
		notice.setText(noticeDetails.getText());
		//notice.setAuthor(noticeDetails.getAuthor());
		//notice.setCreatedDate(LocalDateTime.now());
		noticeDAO.save(notice);
		return "SUCCESS";
	}
	
	// ============================================================== //
	// ProjectEntity CRUD //
	@GetMapping("/api/proj/projectEntity")
	public Iterable<ProjectEntity> getProjectEntityList(){
		return projectEntityDAO.findAll();
	}
	
	@GetMapping("/api/proj/findProjectByUserId")
	public Iterable<ProjectEntity> findProjectByUserId(String userId){
		return projectEntityDAO.findAllByUserId(userId);
	}
	
	@Transactional
	@PostMapping("/api/proj/projectEntity")
	public ProjectEntity createProjectEntity(ProjectEntity param) {
		param.setEnteredDate(new Timestamp(System.currentTimeMillis()));
	    return projectEntityDAO.save(param);
	}
	
	@Transactional
	@DeleteMapping("/api/proj/projectEntity/{pk}")
	public String deleteProjectEntity(@PathVariable Long pk) {
		projectEntityDAO.deleteById(pk);
	    return "SUCCESS";
	}
	
	// =============================================================== //
	
	// ProjectInfo CRUD //
	@GetMapping("/api/proj/projectInfo")
	public Iterable<ProjectInfo> getProjectInfoList(){
		return projectInfoDAO.findAll();
	}
	
	@Transactional
	@PostMapping("/api/proj/projectInfo")
	public ProjectInfo createProjectInfo(ProjectInfo param) {
		param.setCreatedDate(new Timestamp(System.currentTimeMillis()));
	    return projectInfoDAO.save(param);
	}
	
	@Transactional
	@DeleteMapping("/api/proj/projectInfo/{pk}")
	public String deleteProjectInfo(@PathVariable Long pk) {
		projectInfoDAO.deleteById(pk);
	    return "SUCCESS";
	}
	
	@Transactional
	@DeleteMapping("/api/proj/deleteProject/")
	public String deleteProject(@PathVariable Long pk) {
		//projectEntityDAO.delete(entity);
		String deleteStatus = deleteProjectInfo(pk);
	    return deleteStatus;
	}
	
	@Transactional
	@PutMapping("/api/proj/projectInfo/{pk}")
	public String updateProject(@PathVariable Long pk, ProjectInfo updatedProjectInfo) {
		ProjectInfo projectInfo = projectInfoDAO.findById(pk).orElse(null); 
		
		if(projectInfo == null) return "FAIL";
				
		projectInfo.setProjectName(updatedProjectInfo.getProjectName());
		projectInfo.setProjectDescription(updatedProjectInfo.getProjectDescription());
		//projectInfo.setMaster(updatedProjectInfo.getMaster());

		projectInfoDAO.save(projectInfo);
		return "SUCCESS";
	}
	
	// =============================================================== //
	
	@Transactional
	@GetMapping("/api/proj/invite/{pk}")
	public List<JsonEntity> getInviteList(@PathVariable Long pk) {
		List<JsonEntity> res= new ArrayList<JsonEntity>();
		List<JsonEntity> userIdList = Arrays.asList(getUserList());
		Iterable<String> findUserIdByProjectId = projectEntityDAO.findUserIdByProjectId(pk);
		for(JsonEntity userIdAndName : userIdList) {
			boolean entity = false;
			for(String userId : findUserIdByProjectId) {
					if(userIdAndName.getId().equals(userId)) {
						entity = true;
						break;
					}
			}
			if(!entity) res.add(userIdAndName);
		}
	    return res;
	}
	
	@Transactional
	@PostMapping("/api/proj/invite/{pk}")
	public void createProjectEntityByinvite(@PathVariable Long pk, @RequestBody String param) {
		String[] userid=param.split(":");
		for(int i=0; i<userid.length; i++) {
			ProjectEntity newEntity = new ProjectEntity();
			newEntity.setUserId(userid[i]);
			newEntity.setProjectId(pk);
			newEntity.setProjectName(projectInfoDAO.findProjectNameById(pk));
			newEntity.setEnteredDate(new Timestamp(System.currentTimeMillis()));
			projectEntityDAO.save(newEntity);
		}
	}
	
	@GetMapping("/api/proj/getUserList")
	public JsonEntity[]  getUserList(){
		String url = "http://spring-login.istio.svc.cluster.local:8000/api/getUserIdAnNameList";
		final JsonEntity[] response = restTemplate.getForObject(url, JsonEntity[].class);
		return response;
	}
	
	@Transactional
	@PostMapping("/api/proj/projectInfo/{masterId}")
	public void createProject(@PathVariable String masterId, @RequestBody String param) {
		String[] projectData=param.split(":");
		ProjectInfo newProject = new ProjectInfo();
		newProject.setProjectName(projectData[0]);
		newProject.setProjectDescription(projectData[1]);
		newProject.setMaster(masterId.toString());
		newProject.setCreatedDate(new Timestamp(System.currentTimeMillis()));
	    projectInfoDAO.save(newProject);
	    
	    ProjectEntity newEntity = new ProjectEntity();
		newEntity.setUserId(masterId);
		newEntity.setProjectName(projectInfoDAO.findProjectNameById(newProject.getProjectId()));
		newEntity.setEnteredDate(new Timestamp(System.currentTimeMillis()));
		newEntity.setProjectId(newProject.getProjectId());
		projectEntityDAO.save(newEntity);
		
		for(int i=2; i<projectData.length; i++) {
			ProjectEntity inviteEntity = new ProjectEntity();
			inviteEntity.setUserId(projectData[i]);
			inviteEntity.setProjectName(projectInfoDAO.findProjectNameById(newProject.getProjectId()));
			inviteEntity.setEnteredDate(new Timestamp(System.currentTimeMillis()));
			inviteEntity.setProjectId(newProject.getProjectId());
			projectEntityDAO.save(inviteEntity);
		}
	}
	
}
