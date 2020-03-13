package com.example.demo;

import java.util.List;

import javax.transaction.Transactional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UserController {
	@Autowired
	private UserDAO userDAO;
	
	@Transactional
	@PostMapping("/logincheck")
	public String checkUser(UserEntity param) {
		//check user
		System.out.println(param.getId()+" "+param.getPassword());
		UserEntity user=userDAO.findOne(param.getId());
		if (user.getPassword().equals(param.getPassword())){
			System.out.println("SUCCESS");
			return "SUCCESS";
		}else {
			System.out.println("FALSE");
			return "FALSE";
		}
//	    return userDAO.save(param);
	}
	
	@GetMapping("/api/getUserList")
	public Iterable<UserEntity> getUserList(){
		return userDAO.findAll();
	}
	
	@GetMapping("/api/getUserIdList")
	public Iterable<String> getUserIdList(){
		return userDAO.getIdAll();
	}
	
	@GetMapping("/api/getUserIdAnNameList")
	public List<UserIdAndName> getUserIdAnNameList(){
		return userDAO.findAllIdAndName();
	}
	
}
