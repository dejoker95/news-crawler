package org.newsapp.controller.task;


import lombok.RequiredArgsConstructor;
import org.newsapp.domain.task.Task;
import org.newsapp.dto.task.TaskRequestDTO;
import org.newsapp.dto.task.TaskResponseDTO;
import org.newsapp.service.task.TaskService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/tasks")
public class TaskController {

    private final TaskService taskService;

    @GetMapping("/{id}")
    public ResponseEntity<TaskResponseDTO> getTaskById(@PathVariable Long id) {
        Task task = taskService.findById(id);
        return ResponseEntity.ok().body(new TaskResponseDTO(task));
    }

    @GetMapping
    public ResponseEntity<List<TaskResponseDTO>> findAllTasks() {
        List<TaskResponseDTO> tasks = taskService.findAll()
                .stream()
                .map(TaskResponseDTO::new)
                .toList();
        return ResponseEntity.ok().body(tasks);
    }

    @PostMapping
    public ResponseEntity<TaskResponseDTO> addTask(@RequestBody TaskRequestDTO request) {
        Task task = taskService.save(request);
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(new TaskResponseDTO(task));
    }

    @PutMapping("/{id}")
    public ResponseEntity<TaskResponseDTO> updateTask(@PathVariable Long id, @RequestBody TaskRequestDTO request) {
        Task task = taskService.update(id, request);
        return ResponseEntity
                .ok()
                .body(new TaskResponseDTO(task));
    }

    @PostMapping("/{id}/run")
    public ResponseEntity<Void> runTask(@PathVariable Long id) {
        return ResponseEntity.ok().build();
    }

}
