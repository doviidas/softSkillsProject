package com.example.backend.controller;

import com.example.backend.model.StudentProfile;
import com.example.backend.repository.StudentProfileRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@CrossOrigin(origins = "http://localhost:3000") // Adjust if your front-end is hosted elsewhere
@RestController
@RequestMapping("/api/student")
public class StudentProfileController {

    @Autowired
    private StudentProfileRepository studentProfileRepository;

    @GetMapping("/{id}")
    public ResponseEntity<StudentProfile> getStudentProfile(@PathVariable Long id) {
        Optional<StudentProfile> studentProfile = studentProfileRepository.findById(id);
        return studentProfile
                .map(profile -> ResponseEntity.ok(profile))
                .orElseGet(() -> ResponseEntity.notFound().build());
    }
    @PostMapping
    public ResponseEntity<StudentProfile> createStudentProfile(@RequestBody StudentProfile studentProfile) {
        StudentProfile savedProfile = studentProfileRepository.save(studentProfile);
        return new ResponseEntity<>(savedProfile, HttpStatus.CREATED);
    }
}
