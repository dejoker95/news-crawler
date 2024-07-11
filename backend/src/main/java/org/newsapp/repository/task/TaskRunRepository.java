package org.newsapp.repository.task;

import org.newsapp.domain.task.TaskRun;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TaskRunRepository extends JpaRepository<TaskRun, Long> {
}
