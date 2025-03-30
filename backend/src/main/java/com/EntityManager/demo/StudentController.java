package com.EntityManager.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;


import java.util.List;

@RestController
@RequestMapping("/students")
public class StudentController {

    @Autowired
    private StudentService studentService;

    @PostMapping
    public Student save(@RequestBody Student student) {
        return studentService.saveStudent(student);
    }

    @GetMapping("/{id}")
    public Student get(@PathVariable Long id) {
        return studentService.getStudentById(id);
    }
    @GetMapping
    public List<Student> getALl() {
        return studentService.findAll();
    }

    @PutMapping("/{id}")
    public Student update(@PathVariable Long id, @RequestParam String dept) {
        return studentService.updateStudent(id, dept);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        studentService.deleteStudent(id);
    }

    @GetMapping("/by-dept")
    public List<Student> getByDept(@RequestParam String dept) {
        return studentService.findByDepartment(dept);
    }
}
