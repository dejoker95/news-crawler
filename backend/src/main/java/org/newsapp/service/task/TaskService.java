package org.newsapp.service;

import lombok.RequiredArgsConstructor;
import org.newsapp.domain.task.Task;
import org.newsapp.dto.task.TaskRequestDTO;
import org.newsapp.repository.TaskRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@RequiredArgsConstructor
@Service
public class TaskService {

    private final TaskRepository taskRepository;

    public Task findById(Long id) {
        return taskRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("task id not found: " + id));
    }

    @Transactional
    public Task update(Long id, TaskRequestDTO request) {
        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("task id not found: " + id));
        task.update(request);
        return task;
    }

    public List<Task> findAll() {
        return taskRepository.findAll();
    }

    public Task save(TaskRequestDTO request) {
        return taskRepository.save(request.toEntity());
    }

    @Transactional
    public void runTask(Long id) {
        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("task id not found: " + id));

    }
}
