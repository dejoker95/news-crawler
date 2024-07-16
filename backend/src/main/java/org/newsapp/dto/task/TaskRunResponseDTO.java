package org.newsapp.dto.task;


import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.newsapp.domain.task.TaskRun;

import java.time.ZonedDateTime;

@NoArgsConstructor
@AllArgsConstructor
@Getter
public class TaskRunResponseDTO {

    private Long id;
    private String taskName;
    private Long taskHours;
    private String status;
    private ZonedDateTime createdAt;
    private ZonedDateTime finishedAt;
    private Long success;
    private Long failed;

    public TaskRunResponseDTO(TaskRun taskRun) {
        this.id = taskRun.getId();
        this.taskName = taskRun.getTask().getName();
        this.taskHours = taskRun.getTask().getHours();
        this.status = taskRun.getStatus().toString();
        this.createdAt = taskRun.getCreatedAt();
        this.finishedAt = taskRun.getFinishedAt();
        this.success = taskRun.getSuccess();
        this.failed = taskRun.getFailed();
    }
}
