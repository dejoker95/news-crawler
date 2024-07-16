package org.newsapp.service.task;

import lombok.RequiredArgsConstructor;
import org.newsapp.domain.task.TaskRun;
import org.newsapp.dto.task.UpdateTaskRunDTO;
import org.newsapp.repository.task.TaskRunRepository;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@RequiredArgsConstructor
@Service
public class TaskRunService {

    private final TaskRunRepository repository;
    private final RedisTemplate<String, String> redisTemplate;

    public List<TaskRun> findAll() {
        return repository.findAll();
    }

    public void deleteById(Long id) {
        repository.deleteById(id);
    }

    @Transactional
    public TaskRun update(Long id, UpdateTaskRunDTO request) {
        TaskRun taskRun = repository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("id not found: " + id));
        taskRun.update(request);
        return taskRun;
    }
}
