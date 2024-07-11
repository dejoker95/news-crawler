package org.newsapp.service.task;

import lombok.RequiredArgsConstructor;
import org.newsapp.domain.task.TaskRun;
import org.newsapp.repository.task.TaskRunRepository;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.List;

@RequiredArgsConstructor
@Service
public class TaskRunService {

    private final TaskRunRepository repository;
    private final RedisTemplate<String, String> redisTemplate;

    public List<TaskRun> findAll() {
        return repository.findAll();
    }

    public TaskRun save(){
        return
    }

    public void runTask()

    public void addTaskToStream(Long taskId) {

    }
}
