package com.EntityManager.demo;

import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class StudentService {

    @PersistenceContext
    private EntityManager entityManager;

    @Transactional  // ✅ Required for persist()
    public Student saveStudent(Student student) {
        entityManager.persist(student);
        return student;
    }

    public Student getStudentById(Long id) {
        return entityManager.find(Student.class, id);
    }

    @Transactional  // ✅ Required for update operations
    public Student updateStudent(Long id, String newDept) {
        Student student = entityManager.find(Student.class, id);
        if (student != null) {
            student.setDepartment(newDept);
            entityManager.merge(student);
        }
        return student;
    }

    @Transactional  // ✅ Required for delete
    public void deleteStudent(Long id) {
        Student student = entityManager.find(Student.class, id);
        if (student != null) {
            entityManager.remove(student);
        }
    }

    public List<Student> findByDepartment(String dept) {
        String jpql = "SELECT s FROM Student s WHERE s.department = :dept";
        return entityManager.createQuery(jpql, Student.class)
                .setParameter("dept", dept)
                .getResultList();
    }

    public List<Student> findAll() {
        String jpql = "SELECT s FROM Student s";
        return entityManager.createQuery(jpql, Student.class)
                .getResultList();
    }
}
