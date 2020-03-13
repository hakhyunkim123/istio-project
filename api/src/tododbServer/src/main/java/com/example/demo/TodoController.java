package com.example.demo;

import javax.transaction.Transactional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TodoController {
	@Autowired
	private TodoDAO todoDAO;
	
	@GetMapping("/todo/list")
	public Iterable<TodoEntity> getList(){
		return todoDAO.findAll();
	}
	
	@Transactional
	@PostMapping("/todo/createTodo")
	public TodoEntity addBook(TodoEntity param) {
		//create todo
	    return todoDAO.save(param);
	}
	
	@Transactional
	@DeleteMapping("/todo/doneTodo/{pk}")
	public String deleteBook(@PathVariable Long pk) {
	    // delete todo
		todoDAO.deleteById(pk);
	    return "SUCCESS";
	}
}
