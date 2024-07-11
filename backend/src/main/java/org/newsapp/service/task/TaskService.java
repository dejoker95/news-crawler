package org.newsapp.service.task;

import lombok.RequiredArgsConstructor;
import org.newsapp.domain.task.Task;
import org.newsapp.domain.task.TaskRun;
import org.newsapp.dto.task.TaskRequestDTO;
import org.newsapp.repository.task.TaskRepository;
import org.newsapp.repository.task.TaskRunRepository;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RequiredArgsConstructor
@Service
public class TaskService {

    private final TaskRepository taskRepository;
    private final TaskRunRepository taskRunRepository;
    private final RedisTemplate<String, String> redisTemplate;

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
        TaskRun taskRun = taskRunRepository.save(new TaskRun(task));

        Map<String, String> taskMap = new HashMap<>();
        taskMap.put("")
    }
}
