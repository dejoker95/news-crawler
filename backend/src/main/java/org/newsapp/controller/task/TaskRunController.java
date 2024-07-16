package org.newsapp.controller.task;

import lombok.RequiredArgsConstructor;
import org.newsapp.domain.task.TaskRun;
import org.newsapp.dto.task.TaskRunResponseDTO;
import org.newsapp.dto.task.UpdateTaskRunDTO;
import org.newsapp.service.task.TaskRunService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/taskruns")
public class TaskRunController {

    private final TaskRunService service;

    @GetMapping
    public ResponseEntity<List<TaskRunResponseDTO>> findAll() {
        List<TaskRunResponseDTO> dtoList = service.findAll().stream()
                .map(TaskRunResponseDTO::new)
                .toList();
        return ResponseEntity.ok().body(dtoList);
    }

    @PostMapping("{id}/status")
    public ResponseEntity<TaskRunResponseDTO> updateStatus(@PathVariable Long id, @RequestBody UpdateTaskRunDTO request) {
        TaskRun taskRun = service.update(id, request);
        TaskRunResponseDTO dto = new TaskRunResponseDTO(taskRun);
        return ResponseEntity.ok().body(dto);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteById(@PathVariable Long id) {
        service.deleteById(id);
        return ResponseEntity.ok().build();
    }


}
